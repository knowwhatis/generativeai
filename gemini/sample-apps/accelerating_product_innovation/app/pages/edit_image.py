"""
This module manages the image editing page within a Streamlit application.
It provides the following features:

* Image Upload Handling: Processes and stores uploaded images.
* Interactive Image Editor:
    * Offers an interface for modifying images (drawing, background editing, etc.).
    * Processes and combines foreground edits with the background image.
* Draft Saving: Enables saving edited images as drafts, replacing the original draft versions.
* Image Suggestion Generation:
    * Accepts text prompts to generate variations of the edited image.
    * Displays the generated image suggestions.
"""

import logging

from PIL import Image
from app.pages_utils.utils_config import PAGES_CFG
from app.pages_utils.utils_edit_image import (
    handle_image_upload,
    initialize_edit_page_state,
    process_foreground_image,
    save_draft_image,
)
from app.pages_utils.utils_editor_ui import ImageEditor
from app.pages_utils.utils_generate_image_suggestions import (
    generate_suggested_images,
    render_suggested_images,
)
import app.pages_utils.utils_styles as utils_styles
import streamlit as st

# Initialize the state of the edit page
initialize_edit_page_state()

# Get the configuration for the edit page
page_cfg = PAGES_CFG["Editor"]

# Set the page configuration
st.set_page_config(
    page_title=page_cfg["page_title"], page_icon=page_cfg["page_icon"]
)

# Apply the sidebar style
utils_styles.sidebar_apply_style(
    style=utils_styles.STYLE_SIDEBAR,
    image_path=page_cfg["sidebar_image_path"],
)

# Set up logging
logging.basicConfig(
    format="%(levelname)s:%(message)s", level=logging.DEBUG
)

# Check if the user has uploaded an image
if st.session_state.uploaded_img is True:
    handle_image_upload()

# Check if the user has started editing the image
if (
    st.session_state.start_editing is None
    or st.session_state.start_editing is True
):
    # Initialize Editor
    image_editor = ImageEditor()

    # Display the image editor UI
    canvas_result, bg_image, image_bytes = image_editor.display_ui()
    background = Image.new("RGB", bg_image.size)

    # Display save button only if draft elements exist
    # Function of save button: replace the original image in drafts with edited image
    if st.session_state.draft_elements is not None:
        if st.button("Save"):
            row = st.session_state.image_edit_row
            col = st.session_state.image_edit_col
            image = bg_image
            drafts = st.session_state.draft_elements

            save_draft_image(row, col, image, drafts)

    # Check if drawing exists on the canvas (i.e., not blank)
    if (
        canvas_result.image_data is not None
        and canvas_result.image_data.any()
    ):
        # Convert canvas data to a PIL Image object
        foreground = Image.fromarray(canvas_result.image_data)

        # Call image processing function, using canvas drawing as foreground
        processed_image_bytes = process_foreground_image(
            foreground_image=foreground,
            background_image=background,  # Assuming 'background' is defined elsewhere
            bg_editing=st.session_state.bg_editing,
        )
        # Store the processed image data for further use
        st.session_state.mask_image = processed_image_bytes

    # If the prompt to generate edited images has been submitted
    if st.session_state.generate_images is True:
        generate_suggested_images(
            st.session_state.image_prompt,
            image_bytes,
            st.session_state.mask_image,
        )

    # If the image generation is complete, render suggestion on ui
    if st.session_state.suggested_images is not None:
        render_suggested_images(
            st.session_state.suggested_images,
            st.session_state.generated_image,
        )
