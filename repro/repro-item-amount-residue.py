"""Minimal reproduction for the "empty supply box amount is read as 70" bug.

Usage (run from the repository root, OCR service must be reachable):

    python repro-item-amount-residue.py box_big_untrimmed.png

The attached crop is the real 36x22 amount slot of the third (100-point) supply
box, taken from an in-game ActionPoint panel screenshot at native 1280x720.
No stub is involved: the crop goes straight into the same CnOCR model the game
uses, and the first pass reads '70' although the box is empty.
"""
import sys

import cv2

from module.base.utils import crop_to_text
from module.statistics.item import AmountOcr


def main(path):
    image = cv2.imread(path)
    if image is None:
        raise SystemExit(f'cannot read {path}')

    ocr = AmountOcr([], threshold=96, name='repro')
    print(f'input    : {path} {image.shape}')
    print(f'alphabet : {ocr.alphabet}')

    pre = ocr.pre_process(image)
    trimmed = crop_to_text(pre)
    untrimmed_text = ocr.cnocr.atomic_ocr_for_single_lines([pre], ocr.alphabet)[0]
    trimmed_text = ocr.cnocr.atomic_ocr_for_single_lines([trimmed], ocr.alphabet)[0]
    print(f'untrimmed: {untrimmed_text!r}   (this is what the current amount OCR sends first)')
    print(f'trimmed  : {trimmed_text!r}   (what the retry path in this PR ends up sending)')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'box_big_untrimmed.png')
