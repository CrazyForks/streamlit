# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import streamlit as st
from streamlit import runtime
from streamlit.delta_generator import DeltaGenerator

# st.session_state can only be used in streamlit
if runtime.exists():

    def on_click(x, y):
        if "click_count" not in st.session_state:
            st.session_state.click_count = 0

        st.session_state.click_count += 1
        st.session_state.x = x
        st.session_state.y = y

    i1 = st.button(
        "button 1", key="button", on_click=on_click, args=(1,), kwargs={"y": 2}
    )
    st.write("value:", i1)
    st.write("value from state:", st.session_state["button"])

    button_was_clicked = "click_count" in st.session_state
    st.write("Button was clicked:", button_was_clicked)

    if button_was_clicked:
        st.write("times clicked:", st.session_state.click_count)
        st.write("arg value:", st.session_state.x)
        st.write("kwarg value:", st.session_state.y)

i2 = st.checkbox("reset button return value")

i3 = st.button("button 2 (disabled)", disabled=True)
st.write("value 2:", i3)

i4 = st.button("button 3 (primary)", type="primary")
st.write("value 3:", i4)

i5 = st.button("button 4 (primary + disabled)", type="primary", disabled=True)
st.write("value 4:", i5)

st.button("button 5 (container_width)", use_container_width=True)

st.button(
    "button 6 (container_width + help)", use_container_width=True, help="help text"
)

st.button(
    ":material/search: _button 7_ (**styled** :green[label]) :material/arrow_forward:"
)

st.button(
    "button 8 (just help)",
    help="help text",
)

st.button("Like Button", icon=":material/thumb_up:")
st.button("Star Button", icon="⭐")

st.button("Tertiary Button", type="tertiary")
st.button("Disabled Tertiary Button", type="tertiary", disabled=True)

# We add this to test a regression that was happened previously
# because of unused icon name processing
# See: https://github.com/streamlit/streamlit/pull/10247#issuecomment-2612956073
st.button("Button with material icon containing a digit", icon=":material/1k:")
st.button("Button with material icon containing a digit in label :material/1k:")


cols = st.columns(3)

# Order of conn_types matters to preserve the order in st_button.spec.js and the snapshot
conn_types = [
    "snowflake",
    "bigquery",
    "huggingface",
    "aws_s3",
    "http_file",
    "postgresql",
    "gsheets",
    "custom",
]
for i in range(len(conn_types)):
    cols[i % 3].button(conn_types[i], use_container_width=True)


def stylable_container(key: str, css_styles: str | list[str]) -> "DeltaGenerator":
    """
    Insert a container into your app which you can style using CSS.
    This is useful to style specific elements in your app.

    Args:
        key (str): The key associated with this container. This needs to be unique since all styles will be
            applied to the container with this key.
        css_styles (str | List[str]): The CSS styles to apply to the container elements.
            This can be a single CSS block or a list of CSS blocks.

    Returns:
        DeltaGenerator: A container object. Elements can be added to this container using either the 'with'
            notation or by calling methods directly on the returned object.
    """

    class_name = re.sub(r"[^a-zA-Z0-9_-]", "-", key.strip())
    class_name = f"st-key-{class_name}"

    if isinstance(css_styles, str):
        css_styles = [css_styles]

    # Remove unneeded spacing that is added by the html:
    css_styles.append(
        """
> div:first-child {
margin-bottom: -1rem;
}
"""
    )

    style_text = """
<style>
"""

    for style in css_styles:
        style_text += f"""

.st-key-{class_name} {style}
"""

    style_text += """
    </style>
"""

    container = st.container(key=class_name)
    container.html(style_text)
    return container


with stylable_container(
    key="green_button",
    css_styles="""
        button {
            background-color: green;
            color: white;
            border-radius: 20px;
        }
        """,
):
    st.button("Green button")

st.button("Normal button")

with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
        }
        """,
):
    st.markdown("This is a container with a border.")
