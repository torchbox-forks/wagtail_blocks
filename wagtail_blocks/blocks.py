import json

from django import forms
from wagtail.images.blocks import ImageChooserBlock

from wagtail import blocks


class HeaderChoiceBlock(blocks.ChoiceBlock):
    choices = (
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
    )


class HeaderBlock(blocks.StructBlock):
    header = HeaderChoiceBlock(
        label='Header Size',
    )
    text = blocks.CharBlock(
        label='Text',
        max_length=50,
    )

    class Meta:
        template = 'wagtail_blocks/header.html'
        icon = "title"


class ListBlock(blocks.StructBlock):
    content = blocks.ListBlock(
        blocks.CharBlock(),
        label='Items',
    )

    class Meta:
        template = 'wagtail_blocks/list.html'
        icon = "list-ul"


class ImageTextOverlayBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )
    text = blocks.CharBlock(
        label='Text',
        max_length=200,
    )

    class Meta:
        template = 'wagtail_blocks/image_text_overlay.html'
        icon = 'image'


class SingleImageWithText(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )
    text = blocks.CharBlock(
        label='Text',
        max_length=200,
    )


class CroppedImagesWithTextBlock(blocks.StructBlock):
    image_items = blocks.ListBlock(
        SingleImageWithText(),
        label="Image Item",
    )

    class Meta:
        template = 'wagtail_blocks/cropped_images_with_text.html'
        icon = 'camera-retro'


class SingleListImage(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )
    title = blocks.CharBlock(
        label='Title',
        max_length=200,
    )
    text = blocks.CharBlock(
        label='Text',
        max_length=200,
    )
    link_text = blocks.CharBlock(
        label='Link Text',
        max_length=200,
        required=False,
    )
    link_url = blocks.URLBlock(
        label='Link URL',
        max_length=200,
        required=False,
    )


class ListWithImagesBlock(blocks.StructBlock):
    list_items = blocks.ListBlock(
        SingleListImage(),
        label="List Item",
    )

    class Meta:
        template = 'wagtail_blocks/list_with_images.html'
        icon = 'id-card-clip'


class SingleThumbnail(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )


class ThumbnailGalleryBlock(blocks.StructBlock):
    image_items = blocks.ListBlock(
        SingleThumbnail(),
        label="Image",
    )

    class Meta:
        template = 'wagtail_blocks/thumbnail_gallery.html'
        icon = 'object-ungroup'


class ChartChoiceBlock(blocks.ChoiceBlock):
    choices = (
        ('bar', 'Bar'),
        ('horizontalBar', 'Horizontal Bar'),
        ('pie', 'Pie'),
        ('doughnut', 'Doughnut'),
        ('polarArea', 'Polar Area'),
        ('radar', 'Radar'),
        ('line', 'Line'),
    )


class ChartDataset(blocks.StructBlock):
    label = blocks.CharBlock(
        label='Dataset Label',
        max_length=120,
        default='Dataset #1',
    )
    dataset_data = blocks.ListBlock(
        blocks.IntegerBlock(),
        label='Data',
        default='0',
    )


class ChartBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label='Title',
        max_length=120,
        default='Chart Title',
    )
    chart_type = ChartChoiceBlock(
        label='Chart Type',
        default='bar'
    )
    labels = blocks.ListBlock(
        blocks.CharBlock(max_length=40, label="Label", default='Label'),
        label='Chart Labels',
    )
    datasets = blocks.ListBlock(
        ChartDataset(),
        label='Dataset',
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        # Adjusting the shape of the dataset and label
        # TODO: Update this accordingly if the ChartBlock changes its shape or if Wagtail has breaking changes

        value['datasets'] = json.dumps([
            {
                "label": child_value["value"]["label"],
                "dataset_data": [data_item["value"] for data_item in child_value["value"]["dataset_data"]]
            } for child in value['datasets'].bound_blocks if (child_value := child.get_prep_value())
        ])

        value['labels'] = json.dumps([
            child_value['value'] for child in value['labels'].bound_blocks
            if (child_value := child.get_prep_value())
        ])

        return context

    class Meta:
        template = 'wagtail_blocks/chart.html'
        icon = 'chart-column'


class MapBlock(blocks.StructBlock):
    marker_title = blocks.CharBlock(max_length=120,
                                    default="Marker Title 'This will be updated after you save changes.'")
    marker_description = blocks.RichTextBlock()
    zoom_level = blocks.IntegerBlock(min_value=0, max_value=18, default='2', required=False)
    location_x = blocks.FloatBlock(default='35.0', required=False)
    location_y = blocks.FloatBlock(default='0.16', required=False)
    marker_x = blocks.FloatBlock(default='51.5', required=False)
    marker_y = blocks.FloatBlock(default='-0.09', required=False)

    @property
    def media(self):
        return forms.Media(
            js=["https://unpkg.com/leaflet@1.4.0/dist/leaflet.js"],
            css={'all': ["https://unpkg.com/leaflet@1.4.0/dist/leaflet.css"]}
        )

    class Meta:
        form_template = 'wagtail_blocks/admin_blocks/map.html'
        template = 'wagtail_blocks/map.html'
        icon = "globe"


class SingleImageSlide(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )


class ImageSliderBlock(blocks.StructBlock):
    image_items = blocks.ListBlock(
        SingleImageSlide(),
        label="Image",
    )

    class Meta:
        template = 'wagtail_blocks/image_slider.html'
        icon = 'sliders'
