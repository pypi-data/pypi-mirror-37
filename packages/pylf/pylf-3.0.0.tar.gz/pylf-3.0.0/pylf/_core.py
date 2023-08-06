# coding: utf-8
"""The core module"""
import math
import multiprocessing
import random
from typing import *

import PIL.Image
import PIL.ImageColor

from pylf import _exceptions
from pylf import _numeric_ordered_set as _nos
from pylf import _page

# While changing following constants, it is necessary to consider to rewrite the
# relevant codes.
_INTERNAL_MODE = "1"  # The mode for internal computation
_WHITE = 1
_BLACK = 0

_NEWLINE = "\n"

_UNSIGNED_INT32_TYPECODE = "L"
_MAX_INT16_VALUE = 0xFFFF
_STROKE_END = 0xFFFFFFFF


def handwrite(
    text: str,
    backgrounds: Sequence[PIL.Image.Image],
    top_margins: Sequence[int],
    bottom_margins: Sequence[int],
    left_margins: Sequence[int],
    right_margins: Sequence[int],
    line_spacings: Sequence[int],
    font_sizes: Sequence[int],
    word_spacings: Sequence[int],
    line_spacing_sigmas: Sequence[float],
    font_size_sigmas: Sequence[float],
    word_spacing_sigmas: Sequence[float],
    font,
    color: str,
    is_half_char_fn: Callable[[str], bool],
    is_end_char_fn: Callable[[str], bool],
    perturb_x_sigmas: Sequence[float],
    perturb_y_sigmas: Sequence[float],
    perturb_theta_sigmas: Sequence[float],
    worker: int,
    seed: Optional[Hashable],
) -> List[PIL.Image.Image]:
    pages = _draw_pages(
        text=text,
        sizes=tuple(i.size for i in backgrounds),
        top_margins=top_margins,
        bottom_margins=bottom_margins,
        left_margins=left_margins,
        right_margins=right_margins,
        line_spacings=line_spacings,
        font_sizes=font_sizes,
        word_spacings=word_spacings,
        line_spacing_sigmas=line_spacing_sigmas,
        font_size_sigmas=font_size_sigmas,
        word_spacing_sigmas=word_spacing_sigmas,
        font=font,
        is_half_char_fn=is_half_char_fn,
        is_end_char_fn=is_end_char_fn,
        seed=seed,
    )

    renderer = _Renderer(
        backgrounds=backgrounds,
        color=color,
        perturb_x_sigmas=perturb_x_sigmas,
        perturb_y_sigmas=perturb_y_sigmas,
        perturb_theta_sigmas=perturb_theta_sigmas,
        seed=seed,
    )
    if worker == 1:
        return list(map(renderer, pages))
    mp_context = multiprocessing.get_context()
    with mp_context.Pool(worker) as pool:
        return pool.map(renderer, pages)


def _draw_pages(
    text: str,
    sizes: Sequence[Tuple[int, int]],
    top_margins: Sequence[int],
    bottom_margins: Sequence[int],
    left_margins: Sequence[int],
    right_margins: Sequence[int],
    line_spacings: Sequence[int],
    font_sizes: Sequence[int],
    word_spacings: Sequence[int],
    line_spacing_sigmas: Sequence[float],
    font_size_sigmas: Sequence[float],
    word_spacing_sigmas: Sequence[float],
    font,
    is_half_char_fn: Callable[[str], bool],
    is_end_char_fn: Callable[[str], bool],
    seed: Optional[Hashable],
) -> Iterator[_page.Page]:
    assert (
        len(sizes)
        == len(top_margins)
        == len(bottom_margins)
        == len(left_margins)
        == len(right_margins)
        == len(line_spacings)
        == len(font_sizes)
        == len(word_spacings)
        == len(line_spacing_sigmas)
        == len(font_size_sigmas)
        == len(word_spacing_sigmas)
    )

    rand = random.Random(x=seed)
    period = len(sizes)

    iterator = iter(text)
    try:
        char = next(iterator)
        index = 0
        while True:
            width, height = sizes[index % period]

            top = top_margins[index % period]
            bottom = bottom_margins[index % period]
            left = left_margins[index % period]
            right = right_margins[index % period]

            line_spacing = line_spacings[index % period]
            font_size = font_sizes[index % period]
            word_spacing = word_spacings[index % period]

            line_spacing_sigma = line_spacing_sigmas[index % period]
            font_size_sigma = font_size_sigmas[index % period]
            word_spacing_sigma = word_spacing_sigmas[index % period]

            if height < top + line_spacing + bottom:
                raise _exceptions.LayoutError(
                    "The sum of top margin, line spacing and bottom margin"
                    " can not be greater than background's height"
                )

            if font_size > line_spacing:
                raise _exceptions.LayoutError(
                    "Font size can not be greater than line spacing"
                )

            if width < left + font_size + right:
                raise _exceptions.LayoutError(
                    "The sum of left margin, font size and right margin"
                    " can not be greater than background's width"
                )

            if word_spacing <= -font_size // 2:
                raise _exceptions.LayoutError(
                    "Word spacing must be greater than (-font_size // 2)"
                )

            page = _page.Page(
                mode=_INTERNAL_MODE, size=(width, height), color=_BLACK, num=index
            )
            draw = page.draw

            y = top + line_spacing - font_size
            try:
                while y < height - bottom - font_size:
                    x = float(left)
                    while True:
                        if char == _NEWLINE:
                            char = next(iterator)
                            break
                        if x >= width - right - font_size and not is_end_char_fn(char):
                            break
                        xy = (int(x), int(rand.gauss(y, line_spacing_sigma)))
                        font = font.font_variant(
                            size=max(int(rand.gauss(font_size, font_size_sigma)), 0)
                        )
                        offset = _draw_char(draw, char, xy, font)
                        dx = word_spacing + offset * (
                            0.5 if is_half_char_fn(char) else 1
                        )
                        x += rand.gauss(dx, word_spacing_sigma)
                        char = next(iterator)
                    y += line_spacing
            finally:
                yield page
            index += 1
    except StopIteration:
        pass


def _draw_char(draw, char: str, xy: Tuple[int, int], font) -> int:
    """Draws a single char with the parameters and white color, and returns the
    offset."""
    assert len(char) == 1
    draw.text(xy, char, fill=_WHITE, font=font)
    return font.getsize(char)[0]


class _Renderer(object):
    """A callable object rendering the foreground that was drawn text and returning
    rendered image."""

    __slots__ = (
        "_period",
        "_backgrounds",
        "_color",
        "_perturb_x_sigmas",
        "_perturb_y_sigmas",
        "_perturb_theta_sigmas",
        "_rand",
        "_hashed_seed",
    )

    def __init__(
        self,
        backgrounds: Sequence[PIL.Image.Image],
        color: str,
        perturb_x_sigmas: Sequence[float],
        perturb_y_sigmas: Sequence[float],
        perturb_theta_sigmas: Sequence[float],
        seed: Optional[Hashable],
    ) -> None:
        assert (
            len(backgrounds)
            == len(perturb_x_sigmas)
            == len(perturb_y_sigmas)
            == len(perturb_theta_sigmas)
        )
        self._period = len(backgrounds)
        self._backgrounds = backgrounds
        self._color = color
        self._perturb_x_sigmas = perturb_x_sigmas
        self._perturb_y_sigmas = perturb_y_sigmas
        self._perturb_theta_sigmas = perturb_theta_sigmas
        self._rand = random.Random()
        self._hashed_seed = None
        if seed is not None:
            self._hashed_seed = hash(seed)

    def __call__(self, page: _page.Page) -> PIL.Image.Image:
        if self._hashed_seed is None:
            self._rand.seed()  # avoid different processes sharing the same random state
        else:
            self._rand.seed(a=self._hashed_seed + page.num)
        return self._perturb_and_merge(page)

    def _perturb_and_merge(self, page: _page.Page) -> PIL.Image.Image:
        strokes = _extract_strokes(page.matrix, page.image.getbbox())

        x_sigma = self._perturb_x_sigmas[page.num % self._period]
        y_sigma = self._perturb_y_sigmas[page.num % self._period]
        theta_sigma = self._perturb_theta_sigmas[page.num % self._period]
        canvas = self._backgrounds[page.num % self._period].copy()
        fill = PIL.ImageColor.getcolor(self._color, canvas.mode)

        _draw_strokes(
            canvas.load(),
            canvas.size,
            strokes,
            fill,
            x_sigma=x_sigma,
            y_sigma=y_sigma,
            theta_sigma=theta_sigma,
            rand=self._rand,
        )
        return canvas


def _extract_strokes(bitmap, bbox: Tuple[int, int, int, int]) -> _nos.NumericOrderedSet:
    left, upper, right, lower = bbox
    assert left >= 0 and upper >= 0
    assert (
        right <= _MAX_INT16_VALUE and lower < _MAX_INT16_VALUE
    )  # reserve 0xFFFFFFFF as _STROKE_END
    strokes = _nos.NumericOrderedSet(_UNSIGNED_INT32_TYPECODE, privileged=_STROKE_END)
    for y in range(upper, lower):
        for x in range(left, right):
            if bitmap[x, y] and strokes.add(_xy(x, y)):
                _extract_stroke(bitmap, (x, y), strokes, bbox)
                strokes.add(_STROKE_END)
    return strokes


def _extract_stroke(
    bitmap,
    start: Tuple[int, int],
    strokes: _nos.NumericOrderedSet,
    bbox: Tuple[int, int, int, int],
) -> None:
    """Helper function of _extract_strokes() which uses depth first search to find the
    pixels of a glyph."""
    left, upper, right, lower = bbox
    stack = []
    stack.append(start)
    while stack:
        x, y = stack.pop()
        if y - 1 >= upper and bitmap[x, y - 1] and strokes.add(_xy(x, y - 1)):
            stack.append((x, y - 1))
        if y + 1 < lower and bitmap[x, y + 1] and strokes.add(_xy(x, y + 1)):
            stack.append((x, y + 1))
        if x - 1 >= left and bitmap[x - 1, y] and strokes.add(_xy(x - 1, y)):
            stack.append((x - 1, y))
        if x + 1 < right and bitmap[x + 1, y] and strokes.add(_xy(x + 1, y)):
            stack.append((x + 1, y))


def _draw_strokes(
    bitmap,
    size: Tuple[int, int],
    strokes: _nos.NumericOrderedSet,
    fill,
    x_sigma: float,
    y_sigma: float,
    theta_sigma: float,
    rand: random.Random,
) -> None:
    stroke = []
    min_x = _MAX_INT16_VALUE
    min_y = _MAX_INT16_VALUE
    max_x = 0
    max_y = 0
    for xy in strokes:
        if xy == _STROKE_END:
            center = ((min_x + max_x) / 2, (min_y + max_y) / 2)
            _draw_stroke(
                bitmap,
                size,
                stroke,
                center=center,
                fill=fill,
                x_sigma=x_sigma,
                y_sigma=y_sigma,
                theta_sigma=theta_sigma,
                rand=rand,
            )
            min_x = _MAX_INT16_VALUE
            min_y = _MAX_INT16_VALUE
            max_x = 0
            max_y = 0
            stroke.clear()
            continue
        x, y = _x_y(xy)
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
        stroke.append((x, y))


def _draw_stroke(
    bitmap,
    size: Tuple[int, int],
    stroke: Sequence[Tuple[int, int]],
    center: Tuple[float, float],
    fill,
    x_sigma: float,
    y_sigma: float,
    theta_sigma: float,
    rand: random.Random,
) -> None:
    dx = rand.gauss(0, x_sigma)
    dy = rand.gauss(0, y_sigma)
    theta = rand.gauss(0, theta_sigma)
    for x, y in stroke:
        new_x, new_y = _rotate(center, x, y, theta)
        new_x += dx
        new_y += dy
        if 0 <= new_x < size[0] and 0 <= new_y < size[1]:
            bitmap[int(new_x), int(new_y)] = fill


def _rotate(
    center: Tuple[float, float], x: float, y: float, theta: float
) -> Tuple[float, float]:
    new_x = (
        (x - center[0]) * math.cos(theta)
        + (y - center[1]) * math.sin(theta)
        + center[0]
    )
    new_y = (
        (y - center[1]) * math.cos(theta)
        - (x - center[0]) * math.sin(theta)
        + center[1]
    )
    return new_x, new_y


def _xy(x: int, y: int) -> int:
    return (x << 16) + y


def _x_y(xy: int) -> Tuple[int, int]:
    return xy >> 16, xy & 0xFFFF
