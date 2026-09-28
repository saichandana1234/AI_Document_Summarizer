import streamlit as st
from pathlib import Path

from document_parser import extract_text
from summarizer import generate_summary_and_key_points


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Document Summarizer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# Custom Styling
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .info-box {
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">📄 AI Document Summarizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform lengthy documents into clear summaries and important key points using AI.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Features
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "📖 **Smart Summarization**\n\n"
        "Generate concise summaries from documents."
    )

with col2:
    st.info(
        "🔑 **Key Points**\n\n"
        "Extract the most important information."
    )

with col3:
    st.info(
        "📊 **Document Statistics**\n\n"
        "View word counts and summary reduction."
    )


st.divider()


# -----------------------------
# File Upload
# -----------------------------

st.subheader("📤 Upload Your Document")

uploaded_file = st.file_uploader(
    "Supported formats: PDF and DOCX",
    type=["pdf", "docx"]
)


if uploaded_file is not None:

    st.success(
        f"✅ Selected file: {uploaded_file.name}"
    )

    # Create folders
    upload_folder = Path("uploads")
    output_folder = Path("outputs")

    upload_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)

    # Save uploaded file
    file_path = upload_folder / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())


    # -----------------------------
    # Generate Summary Button
    # -----------------------------

    if st.button(
        "✨ Generate Summary",
        type="primary",
        use_container_width=True
    ):

        try:

            # -----------------------------
            # Extract Text
            # -----------------------------

            with st.spinner(
                "📖 Reading your document..."
            ):

                text = extract_text(
                    str(file_path)
                )


            # Check if text was extracted
            if not text.strip():

                st.error(
                    "❌ No readable text was found in this document."
                )

                st.stop()


            original_word_count = len(
                text.split()
            )


            # -----------------------------
            # Generate Summary + Key Points
            # -----------------------------

            with st.spinner(
                "🤖 AI is generating your summary and key points..."
            ):

                summary, key_points = (
                    generate_summary_and_key_points(text)
                )


            summary_word_count = len(
                summary.split()
            )


            # -----------------------------
            # Calculate Reduction
            # -----------------------------

            if original_word_count > 0:

                reduction = (
                    (
                        original_word_count
                        - summary_word_count
                    )
                    / original_word_count
                ) * 100

            else:

                reduction = 0


            st.divider()


            # -----------------------------
            # Document Statistics
            # -----------------------------

            st.subheader(
                "📊 Document Statistics"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Original Words",
                    f"{original_word_count:,}"
                )

            with col2:

                st.metric(
                    "Summary Words",
                    f"{summary_word_count:,}"
                )

            with col3:

                st.metric(
                    "Reduction",
                    f"{reduction:.1f}%"
                )


            st.divider()


            # -----------------------------
            # AI Summary
            # -----------------------------

            st.subheader(
                "📝 AI-Generated Summary"
            )

            st.write(summary)


            st.divider()


            # -----------------------------
            # Key Points
            # -----------------------------

            st.subheader(
                "🔑 Important Key Points"
            )

            st.markdown(key_points)


            st.divider()


            # -----------------------------
            # Save Summary
            # -----------------------------

            output_file = (
                output_folder
                / f"{Path(uploaded_file.name).stem}_summary.txt"
            )


            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "AI DOCUMENT SUMMARY\n"
                )

                file.write(
                    "=" * 50
                )

                file.write(
                    "\n\n"
                )

                file.write(
                    "SUMMARY\n"
                )

                file.write(
                    "-" * 50
                )

                file.write(
                    "\n"
                )

                file.write(
                    summary
                )

                file.write(
                    "\n\n"
                )

                file.write(
                    "KEY POINTS\n"
                )

                file.write(
                    "-" * 50
                )

                file.write(
                    "\n"
                )

                file.write(
                    key_points
                )


            # -----------------------------
            # Download Summary
            # -----------------------------

            st.download_button(
                label="⬇️ Download Summary",
                data=output_file.read_text(
                    encoding="utf-8"
                ),
                file_name=output_file.name,
                mime="text/plain",
                use_container_width=True
            )


            st.success(
                "🎉 Summary generated successfully!"
            )


        # -----------------------------
        # Error Handling
        # -----------------------------

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "AI Document Summarizer • "
    "Built with Python, Streamlit, Gemini AI, "
    "PyMuPDF and python-docx"
)