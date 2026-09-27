from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.models.post_data import PostData

# ============================================================
# TEMPLATE
# ============================================================
WIDTH = 1122
HEIGHT = 1402

# ============================================================
# COLORS
# ============================================================

BLACK = (15, 15, 15)
WHITE = (248, 248, 245)

CREAM = (250, 242, 215)

DATE_BG = (250, 216, 140)

GOLD_BORDER = (240, 180, 45)

RED = (110, 25, 30)
GREEN = (5, 88, 65)
BLUE = (25, 70, 145)

CHANGE_BG = (222, 237, 198)

UP_COLOR = (20, 135, 65)
DOWN_COLOR = (200, 35, 40)
NEUTRAL_COLOR = (85, 85, 85)


# ============================================================
# FONTS
# ============================================================

FONT_REGULAR = (
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans.ttf"
)

FONT_BOLD = (
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans-Bold.ttf"
)


def get_font(size: int, bold: bool = False):

    path = FONT_BOLD if bold else FONT_REGULAR

    return ImageFont.truetype(
        path,
        size,
    )


# ============================================================
# TEXT HELPERS
# ============================================================

def text_size(draw, text, font):

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    return (
        bbox[2] - bbox[0],
        bbox[3] - bbox[1],
    )


def draw_centered(
    draw,
    box,
    text,
    font,
    fill,
):

    x1, y1, x2, y2 = box

    width, height = text_size(
        draw,
        text,
        font,
    )

    x = x1 + (
        (x2 - x1 - width) / 2
    )

    y = y1 + (
        (y2 - y1 - height) / 2
    )

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill,
    )


def draw_fitted_centered(
    draw,
    box,
    text,
    max_size,
    min_size,
    fill,
):

    x1, y1, x2, y2 = box

    selected_font = None

    for size in range(
        max_size,
        min_size - 1,
        -1,
    ):

        current_font = get_font(
            size,
            bold=True,
        )

        width, _ = text_size(
            draw,
            text,
            current_font,
        )

        if width <= (x2 - x1):

            selected_font = current_font
            break

    if selected_font is None:

        selected_font = get_font(
            min_size,
            bold=True,
        )

    draw_centered(
        draw,
        box,
        text,
        selected_font,
        fill,
    )


# ============================================================
# DATE
# ============================================================

def draw_date(
    draw,
    post_data: PostData,
):
    """
    Draw the date cleanly inside the existing date panel.

    The template's calendar icon is preserved. The date/day text
    gets the remaining width so the date occupies the panel properly.
    """

    date_text = post_data.date.strftime("%d %b %Y").upper()
    day_text = post_data.date.strftime("%A").upper()

    # --------------------------------------------------------
    # Date panel
    # --------------------------------------------------------

    panel = (337, 300, 767, 390)

    draw.rounded_rectangle(
        panel,
        radius=22,
        fill=DATE_BG,
    )

    # Preserve/recreate the calendar icon area separately.
    # The text starts after the icon so it never overlaps it.
    text_left = 350
    text_right = 755

    # --------------------------------------------------------
    # Date
    # --------------------------------------------------------

    draw_fitted_centered(
        draw,
        (
            text_left,
            303,
            text_right,
            350,
        ),
        date_text,
        max_size=37,
        min_size=29,
        fill=BLACK,
    )

    # --------------------------------------------------------
    # Day
    # --------------------------------------------------------

    draw_centered(
        draw,
        (
            text_left,
            348,
            text_right,
            382,
        ),
        day_text,
        get_font(18, bold=True),
        BLACK,
    )


# ============================================================
# CLEAR CARD DYNAMIC AREA
# ============================================================

def clear_dynamic_card_area(
    draw,
    box,
):
    """
    Completely removes everything from the dynamic
    portion of the card.

    This is the important fix.

    We clear:

        old rate
        old / gram
        old change
        old placeholder remnants
    """

    x1, y1, x2, y2 = box

    draw.rectangle(
        (
            x1,
            y1,
            x2,
            y2,
        ),
        fill=CREAM,
    )


# ============================================================
# RATE
# ============================================================

def draw_rate(
    draw,
    box,
    rate,
    color,
):

    rate_text = f"₹{rate:,.0f}"

    draw_fitted_centered(
        draw,
        box,
        rate_text,
        max_size=48,
        min_size=30,
        fill=color,
    )


# ============================================================
# CHANGE
# ============================================================

def draw_change(
    draw,
    box,
    diff,
):
    """
    Draw a compact, high-contrast daily change indicator.

    Positive  -> green upward arrow + amount
    Negative  -> red downward arrow + amount
    Neutral   -> grey dash + amount
    """

    x1, y1, x2, y2 = box

    # --------------------------------------------------------
    # Change background
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=20,
        fill=CHANGE_BG,
    )

    # --------------------------------------------------------
    # Determine state
    # --------------------------------------------------------

    if diff > 0:
        symbol = "▲"
        value = f"₹{diff:,.0f}"
        symbol_color = UP_COLOR
        value_color = UP_COLOR

    elif diff < 0:
        symbol = "▼"
        value = f"₹{abs(diff):,.0f}"
        symbol_color = DOWN_COLOR
        value_color = DOWN_COLOR

    else:
        symbol = "—"
        value = "₹0"
        symbol_color = NEUTRAL_COLOR
        value_color = NEUTRAL_COLOR

    # --------------------------------------------------------
    # Fonts
    # --------------------------------------------------------

    symbol_font = get_font(31, bold=True)
    value_font = get_font(50, bold=True)

    # --------------------------------------------------------
    # Measure the top row
    # --------------------------------------------------------

    symbol_width, symbol_height = text_size(
        draw,
        symbol,
        symbol_font,
    )

    value_width, value_height = text_size(
        draw,
        value,
        value_font,
    )

    gap = 10

    total_width = (
        symbol_width * 2
        + gap
        + value_width
    )

    center_x = (x1 + x2) / 2
    start_x = center_x - total_width / 2

    # Vertically center the main change row in the upper part
    # of the pill instead of using fixed offsets.
    top_row_y = y1 + 20

    # --------------------------------------------------------
    # Symbol
    # --------------------------------------------------------

    draw.text(
        (
            start_x,
            top_row_y + 8,
        ),
        symbol,
        font=symbol_font,
        fill=symbol_color,
    )

    # --------------------------------------------------------
    # Value
    # --------------------------------------------------------

    draw.text(
        (
            start_x + symbol_width + gap,
            top_row_y + 2,
        ),
        value,
        font=value_font,
        fill=value_color,
    )

    # --------------------------------------------------------
    # Symbol
    # --------------------------------------------------------

    draw.text(
        (
            start_x + symbol_width + gap + value_width + gap,
            top_row_y + 8,
        ),
        symbol,
        font=symbol_font,
        fill=symbol_color,
    )   


# ============================================================
# COMPLETE DYNAMIC CARD CONTENT
# ============================================================

def draw_dynamic_card_content(
    draw,
    card_box,
    rate,
    diff,
    rate_color,
):
    """
    Redraw the entire dynamic section of a card.

    This is intentionally one operation so there can
    never be old placeholder text underneath.
    """

    x1, y1, x2, y2 = card_box

    # --------------------------------------------------------
    # CLEAR EVERYTHING
    #
    # From below the illustration to the bottom of
    # the dynamic section.
    # --------------------------------------------------------

    clear_dynamic_card_area(
        draw,
        (
            x1 + 5,
            y1,
            x2 - 5,
            y2,
        ),
    )

    # --------------------------------------------------------
    # RATE
    # --------------------------------------------------------

    draw_rate(
        draw,
        (
            x1 + 15,
            y1 + 5,
            x2 - 15,
            y1 + 70,
        ),
        rate,
        rate_color,
    )

    # --------------------------------------------------------
    # / gram
    # --------------------------------------------------------

    draw_centered(
        draw,
        (
            x1,
            y1 + 65,
            x2,
            y1 + 100,
        ),
        "/ gram",
        get_font(
            19,
            bold=True,
        ),
        rate_color,
    )

    # --------------------------------------------------------
    # CHANGE
    # --------------------------------------------------------

    draw_change(
        draw,
        (
            x1 + 15,
            y1 + 105,
            x2 - 15,
            y1 + 205,
        ),
        diff,
    )


# ============================================================
# MAIN RENDERER
# ============================================================

def render_gold_silver_post(
    post_data: PostData,
    template_path: str,
    output_path: str,
):
    print(post_data)

    template = Path(
        template_path
    )

    if not template.exists():

        raise FileNotFoundError(
            f"Template not found: {template}"
        )

    # --------------------------------------------------------
    # Load template
    # --------------------------------------------------------

    image = Image.open(
        template
    ).convert("RGB")

    # --------------------------------------------------------
    # Validate dimensions
    # --------------------------------------------------------

    if image.size != (
        WIDTH,
        HEIGHT,
    ):

        raise ValueError(
            f"Expected template size "
            f"{WIDTH}x{HEIGHT}, "
            f"got {image.size}"
        )

    draw = ImageDraw.Draw(image)

    # ========================================================
    # DATE
    # ========================================================

    draw_date(
        draw,
        post_data,
    )

    # ========================================================
    # 22K GOLD
    # ========================================================

    draw_dynamic_card_content(
        draw,

        # Entire dynamic area of 22K card
        (
            40,
            720,
            370,
            970,
        ),

        post_data.gold22kRate,
        post_data.gold22kDiff,

        RED,
    )

    # ========================================================
    # 24K GOLD
    # ========================================================

    draw_dynamic_card_content(
        draw,

        (
            395,
            720,
            735,
            970,
        ),

        post_data.gold24kRate,
        post_data.gold22kDiff,

        GREEN,
    )

    # ========================================================
    # SILVER
    # ========================================================

    draw_dynamic_card_content(
        draw,

        (
            750,
            720,
            1080,
            970,
        ),

        post_data.silverRate,
        post_data.silverDiff,

        BLUE,
    )

    # ========================================================
    # SAVE
    # ========================================================

    output = Path(
        output_path
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image.save(
        output,
        "PNG",
        optimize=True,
    )

    return str(output)