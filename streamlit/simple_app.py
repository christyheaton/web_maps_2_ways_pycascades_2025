import numpy as np
import pandas as pd
import streamlit as st

st.title("A simple app")
st.write("Let's create a table:")
df = pd.DataFrame(np.random.randint(0, 5, 5))
st.write(df)
st.scatter_chart(df)
