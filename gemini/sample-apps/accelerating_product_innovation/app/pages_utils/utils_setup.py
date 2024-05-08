"""
Common utilities for the project. This includes:
    * session state initialization.
    * project selection.
"""

# pylint: disable=E0401

from typing import Any

from app.pages_utils import utils_project
import streamlit as st


def display_projects() -> None:
    """Displays the list of projects and allows the user to select one.

    Args:
        None

    Returns:
        None
    """
    st.session_state.product_category = st.selectbox(
        "Select a project", st.session_state.product_categories
    )
    st.session_state.product_categories.remove(
        st.session_state.product_category
    )
    st.session_state.product_categories.insert(
        0, st.session_state.product_category
    )
    if (
        st.session_state.previous_product_category
        != st.session_state.product_category
    ):
        reinitialize_session_states()
        st.session_state.previous_product_category = (
            st.session_state.product_category
        )
        st.rerun()


def get_session_state() -> dict:
    """
    Defines default values for session state

    Returns:
        session_state_defaults (dict): A dictionary of default key-value pairs
        for session state
    """
    session_state_defaults: dict[str, Any] = {
        "product_categories": utils_project.get_projects_list(),
        "new_product_category_added": None,
        "previous_product_category": None,
        "text_edit_prompt": None,
        "update_text_btn": None,
        "uploaded_files": None,
        "rag_search_term": None,
        "rag_answers_gen": False,
        "rag_answer": None,
        "rag_answer_references": None,
        "insights_suggestion": None,
        "insights_placeholder": "",
        "suggestion_first_time": 1,
        "processed_data_list": [],
        "query_vectors": [],
        "dff": None,
        "temp_suggestions": None,
        "assorted_prod_title": None,
        "assorted_prod_content": [],
        "email_gen": False,
        "create_product": False,
        "modifying": False,
        "custom_prompt": "",
        "feature_suggestions": None,
        "selected_titles": [],
        "saved_titles": [],
        "selected_prompt": None,
        "product_gen_image": None,
        "features_generated": False,
        "generated_points": None,
        "content_generated": False,
        "product_content": None,
        "image_to_edit": -1,
        "generate_images": False,
        "image_prompt": None,
        "image_file_prefix": "uploaded_image",
        "email_image": None,
        "email_prompt": "High SPF",
        "num_drafts": None,
        "email_text": None,
        "generated_image": None,
        "mask_image": None,
        "edit_suggestion": False,
        "suggested_images": None,
        "uploaded_img": False,
        "start_editing": False,
        "text_to_edit": None,
        "content_edited": None,
        "row": None,
        "edited_content": None,
        "col": None,
        "generated_response": None,
        "draft_elements": None,
        "chosen_titles": [],
        "buffer": None,
        "save_edited_image": None,
        "email_files": [],
        "image_edit_col": None,
        "image_edit_row": None,
        "bg_editing": False,
    }

    return session_state_defaults


def initialize_all_session_state():
    """Initializes all the session states used in the app.

    Args:
        None

    Returns:
        None
    """
    session_state_defaults = get_session_state()
    for key, value in session_state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "product_category" not in st.session_state:
        st.session_state.product_category = (
            st.session_state.product_categories[0]
        )


def reinitialize_session_states():
    """Reinitializes all the session states used in the app.

    Args:
        None

    Returns:
        None
    """

    # Reset state to default.
    session_state_defaults = get_session_state()
    for key, value in session_state_defaults.items():
        st.session_state[key] = value


def page_setup(page_cfg: dict) -> None:
    """
    This function initializes the page configuration and applies custom styles.

    Args:
        page_cfg (dict): A dictionary containing the configuration for the
        page.

    Returns:
        None
    """

    # Set the page configuration
    st.set_page_config(
        page_title=page_cfg["page_title"], page_icon=page_cfg["page_icon"]
    )

    # Initialize session state for the project if it does not exist.
    if (
        "initialize_session_state" not in st.session_state
        or st.session_state.initialize_session_state is False
    ):
        initialize_all_session_state()
        st.session_state.initialize_session_state = True
    # Apply the sidebar style
    load_css("app/css/sidebar_styles.css")


def load_css(css_file_path: str) -> None:
    """
    Load css from the given filepath.
    """
    with open(css_file_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
