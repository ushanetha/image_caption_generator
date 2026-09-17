import streamlit as st
import pandas as pd

from image_processor import ImageProcessor
from caption_generator import CaptionGenerator
from storage_manager import StorageManager


st.set_page_config(
    page_title="Image Caption Generator",
    page_icon="🖼️",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_caption_model():
    return CaptionGenerator()


caption_model = load_caption_model()
storage_manager = StorageManager()


st.markdown(
    "<div class='main-title'>🖼️ Image Caption Generator</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Upload an image and generate an AI-powered descriptive caption</div>",
    unsafe_allow_html=True
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        image = ImageProcessor.load_image(uploaded_file)
        image_details = ImageProcessor.get_image_details(image)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Uploaded Image")
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("Image Information")
            st.metric("Width", f"{image_details['width']} px")
            st.metric("Height", f"{image_details['height']} px")
            st.metric("Channels", image_details["channels"])

        st.divider()

        if st.button("Generate Caption", use_container_width=True):
            with st.spinner("AI is analyzing the image..."):
                caption = caption_model.generate_caption(image)

            st.success("Caption Generated Successfully!")
            st.markdown("### Generated Caption")
            st.info(caption)

            storage_manager.save_result(
                uploaded_file.name,
                caption,
                image_details
            )

            export_text = f"""IMAGE CAPTION RESULT
====================

Filename: {uploaded_file.name}

Caption:
{caption}

Image Details:
Width: {image_details['width']} px
Height: {image_details['height']} px
Channels: {image_details['channels']}
"""

            st.download_button(
                label="Download Caption Result",
                data=export_text,
                file_name="image_caption_result.txt",
                mime="text/plain"
            )

    except Exception as error:
        st.error(f"Error processing image: {error}")

st.divider()
st.subheader("Caption History")

history = storage_manager.load_results()

if history:
    dataframe = pd.DataFrame(history)
    st.dataframe(dataframe, use_container_width=True)

    csv_data = dataframe.to_csv(index=False)

    st.download_button(
        label="Export Complete History as CSV",
        data=csv_data,
        file_name="caption_history.csv",
        mime="text/csv"
    )
else:
    st.info("No caption history available yet.")
