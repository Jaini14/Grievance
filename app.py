import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


from ai_engine import classify_grievance, detect_priority, sentiment_analysis
from database import create_table, insert_grievance, fetch_grievances

# ---------- Page Config ----------
st.set_page_config(
    page_title="LDCE AI Grievance System",
    layout="wide"
)

# ---------- Init DB ----------
create_table()

# ---------- Sidebar ----------
st.sidebar.title("🔐 Login")
role = st.sidebar.selectbox("Login As", ["Student", "Admin"])

# ==================================================
# 🎓 STUDENT MODULE
# ==================================================
if role == "Student":
    st.title("📝 AI-Powered Grievance Submission")

    grievance_text = st.text_area("Enter your grievance")
    anonymous = st.checkbox("Submit Anonymously")

    if st.button("Submit Grievance"):
        if grievance_text.strip() == "":
            st.warning("Please enter grievance text")
        else:
            category = classify_grievance(grievance_text)
            priority = detect_priority(grievance_text)
            sentiment = sentiment_analysis(grievance_text)

            insert_grievance(
                grievance_text,
                category,
                priority,
                sentiment,
                "Yes" if anonymous else "No"
            )

            st.success("✅ Grievance Submitted Successfully")

            st.write("📌 **Detected Category:**", category)
            st.write("⚠ **Priority Level:**", priority)
            st.write("😊 **Sentiment:**", sentiment)
            st.info("📄 Your grievance is now under review")

# ==================================================
# 👨‍💼 ADMIN MODULE
# ==================================================
if role == "Admin":
    st.markdown("## 📊 LDCE Grievance Analytics Dashboard")
    st.caption("AI-powered insights for transparent & efficient grievance governance")

    data = fetch_grievances()
    df = pd.DataFrame(data, columns=[
        "ID", "Text", "Category", "Priority",
        "Sentiment", "Status", "Anonymous", "Date"
    ])

    if df.empty:
        st.warning("No grievances available yet.")
        st.stop()

    # ================= KPI CARDS =================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📨 Total Grievances", len(df))
    col2.metric("🚨 High Priority", len(df[df["Priority"] == "High"]))
    col3.metric("⏳ Pending", len(df[df["Status"] == "Pending"]))
    col4.metric("🕵 Anonymous", len(df[df["Anonymous"] == "Yes"]))

    st.markdown("---")

    # ================= CATEGORY PIE =================
    col5, col6 = st.columns(2)

    with col5:
        fig_cat = px.pie(
            df,
            names="Category",
            title="📌 Grievances by Category",
            hole=0.45
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # ================= PRIORITY BAR =================
    with col6:
        fig_pri = px.bar(
            df,
            x="Priority",
            title="⚠ Priority Distribution",
            color="Priority"
        )
        st.plotly_chart(fig_pri, use_container_width=True)

    st.markdown("---")

    # ================= SENTIMENT ANALYSIS =================
    col7, col8 = st.columns(2)

    with col7:
        fig_sent = px.pie(
            df,
            names="Sentiment",
            title="😊 Sentiment Analysis (AI Detected)",
            color="Sentiment"
        )
        st.plotly_chart(fig_sent, use_container_width=True)

    # ================= MONTHLY TREND =================
    with col8:
        df["Date"] = pd.to_datetime(df["Date"])
        trend = df.groupby(df["Date"].dt.to_period("M")).size().reset_index(name="Count")
        trend["Date"] = trend["Date"].astype(str)

        fig_trend = px.line(
            trend,
            x="Date",
            y="Count",
            title="📈 Monthly Grievance Trend",
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # ================= DEPARTMENT LOAD =================
    dept_count = df["Category"].value_counts().reset_index()
    dept_count.columns = ["Department", "Grievances"]

    fig_dept = px.bar(
        dept_count,
        x="Department",
        y="Grievances",
        title="🏢 Department-wise Workload",
        text="Grievances"
    )
    st.plotly_chart(fig_dept, use_container_width=True)

    st.markdown("---")

    # ================= DATA TABLE =================
    st.subheader("📋 Grievance Management Table")
    st.dataframe(
        df[["ID", "Category", "Priority", "Sentiment", "Status", "Anonymous", "Date"]],
        use_container_width=True
    )


    # ---------- KPIs ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Grievances", len(df))
    col2.metric("Pending", len(df[df["Status"] == "Pending"]))
    col3.metric("Resolved", len(df[df["Status"] == "Resolved"]))

    # ---------- Charts ----------
    st.subheader("📈 Grievance Analytics")

    col4, col5 = st.columns(2)

    with col4:
        pie = px.pie(df, names="Category", title="Category-wise Distribution")
        st.plotly_chart(pie, use_container_width=True)

    with col5:
        bar = px.bar(df, x="Priority", title="Priority-wise Grievances")
        st.plotly_chart(bar, use_container_width=True)

    line = px.line(
        df,
        x="Date",
        title="Monthly Grievance Trend"
    )
    st.plotly_chart(line, use_container_width=True)

    # ---------- Grievance Table ----------
    st.subheader("📋 All Grievances")
    st.dataframe(df, use_container_width=True)
