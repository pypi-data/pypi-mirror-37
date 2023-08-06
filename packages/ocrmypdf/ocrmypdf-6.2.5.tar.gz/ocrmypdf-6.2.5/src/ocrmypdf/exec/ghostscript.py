# © 2017 James R. Barlow: github.com/jbarlow83
#
# This file is part of OCRmyPDF.
#
# OCRmyPDF is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OCRmyPDF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OCRmyPDF.  If not, see <http://www.gnu.org/licenses/>.

from tempfile import NamedTemporaryFile
from subprocess import run, PIPE, STDOUT, CalledProcessError
from shutil import copy
from functools import lru_cache
import re
import sys
from PIL import Image
from . import get_version
from ..exceptions import SubprocessOutputError, MissingDependencyError
from ..helpers import fspath


@lru_cache(maxsize=1)
def version():
    return get_version('gs')


def jpeg_passthrough_available():
    """
    Returns True if the installed version of Ghostscript supports JPEG passthru

    Prior to 9.23, Ghostscript decode and re-encoded JPEGs internally. In 9.23
    it gained the ability to keep JPEGs unmodified. However, the 9.23
    implementation was buggy and would deletes the last two bytes of images in
    some cases, as reported here.
    https://bugs.ghostscript.com/show_bug.cgi?id=699216

    The issue was fixed for 9.24, hence that is the first version we consider
    the feature available. (However, we don't use 9.24 at all, so the first
    version that allows JPEG passthrough is 9.25.

    Regardless, in ocrmypdf 6.x we are ignoring this new feature entirely to
    avoid new behavior.
    """
    return False


def _gs_error_reported(stream):
    return re.search(r'error', stream, flags=re.IGNORECASE)


def rasterize_pdf(input_file, output_file, xres, yres, raster_device, log,
                  pageno=1, page_dpi=None):
    """
    Rasterize one page of a PDF at resolution (xres, yres) in canvas units.

    The image is sized to match the integer pixels dimensions implied by
    (xres, yres) even if those numbers are noninteger. The image's DPI will
     be overridden with the values in page_dpi.

    :param input_file: pathlike
    :param output_file: pathlike
    :param xres: resolution at which to rasterize page
    :param yres:
    :param raster_device:
    :param log:
    :param pageno: page number to rasterize (beginning at page 1)
    :param page_dpi: resolution tuple (x, y) overriding output image DPI
    :return:
    """
    res = xres, yres
    int_res = round(xres), round(yres)
    if not page_dpi:
        page_dpi = res
    with NamedTemporaryFile(delete=True) as tmp:
        args_gs = [
            'gs',
            '-dQUIET',
            '-dSAFER',
            '-dBATCH',
            '-dNOPAUSE',
            '-sDEVICE=%s' % raster_device,
            '-dFirstPage=%i' % pageno,
            '-dLastPage=%i' % pageno,
            '-r{0}x{1}'.format(str(int_res[0]), str(int_res[1])),
            '-o', tmp.name,
            fspath(input_file)
        ]

        p = run(args_gs, stdout=PIPE, stderr=STDOUT,
                universal_newlines=True)
        if _gs_error_reported(p.stdout):
            log.error(p.stdout)
        else:
            log.debug(p.stdout)

        if p.returncode != 0:
            log.error('Ghostscript rasterizing failed')
            raise SubprocessOutputError()

        # Ghostscript only accepts integers for output resolution
        # if the resolution happens to be fractional, then the discrepancy
        # would change the size of the output page, especially if the DPI
        # is quite low. Resize the image to the expected size

        tmp.seek(0)
        with Image.open(tmp) as im:
            expected_size = round(im.size[0] / int_res[0] * res[0]), \
                            round(im.size[1] / int_res[1] * res[1])
            if expected_size != im.size or page_dpi != (xres, yres):
                log.debug(
                    "Ghostscript: resize output image {} -> {}".format(
                        im.size, expected_size))
                im.resize(expected_size).save(
                    fspath(output_file), dpi=page_dpi)
            else:
                copy(tmp.name, fspath(output_file))


def generate_pdfa(pdf_pages, output_file, compression, log,
                  threads=1, pdf_version='1.5', pdfa_part='2'):
    compression_args = []
    if compression == 'jpeg':
        compression_args = [
            "-dAutoFilterColorImages=false",
            "-dColorImageFilter=/DCTEncode",
            "-dAutoFilterGrayImages=false",
            "-dGrayImageFilter=/DCTEncode",
        ]
    elif compression == 'lossless':
        compression_args = [
            "-dAutoFilterColorImages=false",
            "-dColorImageFilter=/FlateEncode",
            "-dAutoFilterGrayImages=false",
            "-dGrayImageFilter=/FlateEncode",
        ]
    else:
        compression_args = [
            "-dAutoFilterColorImages=true",
            "-dAutoFilterGrayImages=true",
        ]

    # Older versions of Ghostscript expect a leading slash in
    # sColorConversionStrategy, newer ones should not have it. See Ghostscript
    # git commit fe1c025d.
    strategy = 'RGB' if version() >= '9.19' else '/RGB'

    if version() >= '9.23':
        # 9.23: new feature JPEG passthrough is broken in some cases, best to
        # disable it always
        # https://bugs.ghostscript.com/show_bug.cgi?id=699216
        # fixed in 9.24, but to avoid changing expected behavior we disable it
        # for ocrmypdf 6.x
        compression_args.append('-dPassThroughJPEGImages=false')

    with NamedTemporaryFile(delete=True) as gs_pdf:
        args_gs = [
            "gs",
            "-dQUIET",
            "-dBATCH",
            "-dNOPAUSE",
            "-dCompatibilityLevel=" + str(pdf_version),
            "-dNumRenderingThreads=" + str(threads),
            "-sDEVICE=pdfwrite",
            "-dAutoRotatePages=/None",
            "-sColorConversionStrategy=" + strategy,
            "-sProcessColorModel=DeviceRGB"
        ] + compression_args + [
            "-dJPEGQ=95",
            "-dPDFA=" + pdfa_part,
            "-dPDFACompatibilityPolicy=1",
            "-sOutputFile=" + gs_pdf.name,
        ]
        args_gs.extend(pdf_pages)
        p = run(args_gs, stdout=PIPE, stderr=STDOUT,
                universal_newlines=True)

        if _gs_error_reported(p.stdout):
            log.error(p.stdout)
        elif 'overprint mode not set' in p.stdout:
            # Unless someone is going to print PDF/A documents on a
            # magical sRGB printer I can't see the removal of overprinting
            # being a problem....
            log.debug(
                "Ghostscript had to remove PDF 'overprinting' from the "
                "input file to complete PDF/A conversion. "
                )
        else:
            log.debug(p.stdout)

        if p.returncode == 0:
            # Ghostscript does not change return code when it fails to create
            # PDF/A - check PDF/A status elsewhere
            copy(gs_pdf.name, output_file)
        else:
            log.error('Ghostscript PDF/A rendering failed')
            raise SubprocessOutputError()
