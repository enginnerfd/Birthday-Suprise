import streamlit as st
import json
from datetime import date, timedelta
import pandas as pd
import os

# تنظیمات صفحه
st.set_page_config(
    page_title="CycleLab | آزمایشگاه چرخه قاعدگی",
    page_icon="🌸",
    layout="wide"
)

# طراحی ظاهری سایت


st.markdown("""
<style>

/* رنگ‌های اصلی */
:root {
    --primary: #8B78C6;
    --primary-light: #EEE9FA;
    --mint: #B9D8CA;
    --background: #F8F7F3;
    --text: #353348;
}

/* پس‌زمینه اصلی */
.stApp {
    background: #F8F7F3;
    color: #353348;
    direction: rtl;
}

/* فضای محتوای اصلی */
.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* منوی کناری */
[data-testid="stSidebar"] {
    background: #EDE7F6;
    border-left: 1px solid #DDD4EB;
}

[data-testid="stSidebar"] * {
    color: #222222 !important;
}

[data-testid="stSidebar"] h1 {
    color: #222222 !important;
}

[data-testid="stSidebar"] h1 {
    color: #7663A4;
}

[data-testid="stSidebar"] * {
    color: #F7F4FF;
}

[data-testid="stSidebar"] h1 {
    color: #D9CDFB;
}

/* عنوان‌ها */
h1 {
    color: #65538F !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #74639F !important;
    font-weight: 700 !important;
}

/* متن‌ها */
p, label {
    color: #49465C;
    line-height: 1.9;
}

/* کارت‌ها */
[data-testid="stMetric"],
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #EAE5F3;
    border-radius: 18px;
    padding: 14px;
}

/* دکمه‌ها */
.stButton > button,
.stDownloadButton > button {
    background: #8B78C6;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #7060A8;
    color: white;
    border: none;
}

/* کادرهای ورودی */
.stTextInput input,
.stTextArea textarea,
.stDateInput input {
    background: white;
    border: 1px solid #DDD5EC;
    border-radius: 12px;
}

/* انتخابگرها */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
}

/* خط جداکننده */
hr {
    border-color: #E7E0F0;
}

/* پیام‌های اطلاع‌رسانی */
[data-testid="stAlert"] {
    border-radius: 14px;
}

/* فاصله بین بخش‌ها */
div[data-testid="stVerticalBlock"] {
    gap: 1rem;
}
/* طراحی منوی کناری */

[data-testid="stSidebar"] {
    background: #F0EBF7;
    border-left: 1px solid #E2D9ED;
}

[data-testid="stSidebar"] [data-testid="stMarkdown"] h2 {
    color: #7663A4;
    text-align: center;
}

/* گزینه‌های منو */
[data-testid="stSidebar"] .stRadio label {
    background: #FAF8FC;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 7px;
    border: 1px solid #E7E0F0;
    transition: 0.2s;
}

/* گزینه انتخاب‌شده */
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: #DED3F1;
    border: 1px solid #BDA9DD;
}

/* نوشته‌ها */
[data-testid="stSidebar"] .stRadio label p {
    color: #292533 !important;
    font-weight: 600;
}
/* انیمیشن ورود صفحات */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.main .block-container {
    animation: fadeIn 0.5s ease;
}

/* افکت کارت‌ها */
.info-card {
    transition: all 0.3s ease;
    cursor: pointer;
}

.info-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(118, 99, 164, 0.18);
    border-color: #BDA9DD;
}

/* افکت دکمه‌ها */
.stButton > button {
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(118, 99, 164, 0.2);
}

/* افکت هدر */
.header-card {
    transition: all 0.3s ease;
}

.header-card:hover {
    box-shadow: 0 8px 20px rgba(118, 99, 164, 0.12);
}
</style>
""", unsafe_allow_html=True)



# عنوان سایت
st.markdown(
    """
    <div style="
        background: linear-gradient(120deg, #d65ca7, #9575cd);
        padding: 30px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 25px;
    ">
        <h1 style="color: white !important; font-size: 42px;">
            🌸 CycleLab
        </h1>
        <p style="color: white; font-size: 18px;">
            آزمایشگاه علمی چرخه قاعدگی و هورمون‌ها
        </p>
        <p style="color: white; font-size: 14px;">
            Understand Your Cycle • Explore Your Hormones
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
به **CycleLab** خوش آمدی!

در این سایت می‌توانیم با مراحل چرخه قاعدگی
و تغییرات هورمون‌های بدن آشنا شویم.
""")

st.divider()
st.markdown("""
<div style="
    background: linear-gradient(135deg, #E9E1F5, #F5EFE6);
    padding: 35px 20px;
    border: 1px solid #E4DCEF;
    border-radius: 24px;
    margin-bottom: 28px;
    text-align: center;
">
    <div style="font-size: 38px;">🌷</div>
    <h1 style="
        color: #7663A4;
        font-size: 34px;
        margin: 8px 0;
    ">
        CycleLab
    </h1>
    <p style="
        color: #71677E;
        font-size: 15px;
        margin: 0;
    ">
        Learn • Explore • Understand
    </p>
    <p style="
        color: #71677E;
        font-size: 13px;
    ">
        آزمایشگاه آموزشی چرخه قاعدگی و هورمون‌ها
    </p>
</div>
""", unsafe_allow_html=True)

def page_header(title, subtitle, emoji):

    st.markdown(f"""
    <div class="header-card" style="
        background: linear-gradient(120deg, #EAE2F5, #F5EFE5);
        border: 1px solid #E2D8EF;
        padding: 25px;
        border-radius: 22px;
        margin-bottom: 25px;
        text-align: center;
    ">
        <div style="font-size:35px;">{emoji}</div>

        <h1 style="
            color:#7663A4;
            font-size:28px;
            margin:8px 0;
        ">
            {title}
        </h1>

        <p style="
            color:#71677E;
            font-size:14px;
            margin:0;
        ">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)
    # وضعیت ورود کاربر
if "entered" not in st.session_state:
    st.session_state.entered = False

# صفحه خوشامدگویی
if not st.session_state.entered:

   

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "🌸 ورود به آزمایشگاه",
            use_container_width=True
        ):
            st.session_state.entered = True
            st.rerun()

    st.markdown("""
    <p style="
        text-align:center;
        color:#94899F;
        font-size:12px;
        margin-top:35px;
    ">
        CycleLab | Educational Project
    </p>
    """, unsafe_allow_html=True)

    st.stop()
# منوی کناری
st.sidebar.markdown(
    """
    <div style="text-align:center; padding:20px 5px;">
        <h1 style="font-size:28px;">🌸 CycleLab</h1>
        <p style="font-size:13px; color:#81458b;">
            Your Hormone Science Lab
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()
st.sidebar.markdown("""
<div style="
    text-align:center;
    padding:20px 10px;
    margin-bottom:15px;
">
    <div style="font-size:35px;">🌷</div>
    <h2 style="color:#7663A4;">CycleLab</h2>
    <p style="color:#777080;font-size:12px;">
        Your Cycle Learning Space
    </p>
</div>
""", unsafe_allow_html=True)
page = st.sidebar.radio(
    "🧭 منوی اصلی",
    [
        "🏠 داشبورد",
        "🩸 چرخه قاعدگی",
        "🧬 آزمایشگاه هورمون‌ها",
        "📊 نمودار هورمونی",
        "📚 کتابخانه علمی",
        "📅 تقویم قاعدگی",
        "📝 ثبت علائم روزانه",
        "🧠 تحلیل هوشمند چرخه",
        "📈 داشبورد گرافیکی",
        "📄 گزارش چرخه",
        "💾 پشتیبان‌گیری اطلاعات",
    ],
    label_visibility="visible"
)

# محتوای صفحات
if page == "🏠 داشبورد":

    st.title("🌷 داشبورد CycleLab")
    st.write("به آزمایشگاه آموزشی چرخه قاعدگی خوش آمدی.")

    st.markdown("""
    <style>
    .info-card {
        background: linear-gradient(135deg, #EEE9FA, #F8F4EC);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #E3D9F0;
        text-align: center;
        min-height: 145px;
        box-shadow: 0 4px 12px rgba(100, 80, 140, 0.08);
    }

    .info-card h3 {
        color: #7663A4;
        font-size: 20px;
    }

    .info-card p {
        color: #484354;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🩸 چرخه قاعدگی</h3>
            <p>آشنایی با مراحل مختلف چرخه</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>🧬 هورمون‌ها</h3>
            <p>شناخت استروژن، پروژسترون، LH و FSH</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>📈 نمودارها</h3>
            <p>مشاهده تغییرات فرضی هورمونی</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="info-card">
            <h3>📚 کتابخانه علمی</h3>
            <p>مطالعه مطالب آموزشی و علمی</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("✨ درباره CycleLab")

    st.write("""
    CycleLab یک محیط آموزشی برای شناخت چرخه قاعدگی،
    تغییرات هورمونی و آشنایی با سلامت بدن است.
    """)

elif page == "🧬 آزمایشگاه هورمون‌ها":

    st.header("🧬 آزمایشگاه هورمون‌ها")

    hormone = st.selectbox(
        "یک هورمون انتخاب کن:",
        ["استروژن", "پروژسترون", "LH", "FSH"]
    )

    hormone_info = {
        "استروژن": (
            "در رشد پوشش داخلی رحم و تنظیم چرخه نقش دارد. "
            "سطح آن در طول چرخه تغییر می‌کند."
        ),
        "پروژسترون": (
            "پس از تخمک‌گذاری، جسم زرد منبع اصلی تولید آن است. "
            "این هورمون به آماده و حفظ شدن پوشش داخلی رحم کمک می‌کند."
        ),
        "LH": (
            "افزایش ناگهانی این هورمون معمولاً باعث تحریک تخمک‌گذاری می‌شود."
        ),
        "FSH": (
            "در رشد و بلوغ فولیکول‌های تخمدان نقش دارد."
        )
    }

    st.subheader(f"🔍 {hormone}")
    st.write(hormone_info[hormone])

elif page == "📊 نمودار هورمونی":

    import pandas as pd
    import numpy as np

    st.header("📊 آزمایشگاه تغییرات هورمونی")

    cycle_length = st.slider(
        "طول چرخه قاعدگی (روز)",
        min_value=21,
        max_value=35,
        value=28
    )

    days = np.arange(1, cycle_length + 1)

    # داده‌های آموزشی و فرضی
    ovulation_day = cycle_length - 14

    estrogen = (
        20
        + 80 * np.exp(-((days - (ovulation_day - 2)) / 4) ** 2)
        + 20 * np.exp(-((days - (ovulation_day + 5)) / 5) ** 2)
    )

    progesterone = (
        10
        + 80 / (1 + np.exp(-(days - ovulation_day) / 2))
        - 70 / (1 + np.exp(-(days - (cycle_length - 3)) / 2))
    )

    lh = (
        10
        + 100 * np.exp(-((days - ovulation_day) / 1.3) ** 2)
    )

    fsh = (
        25
        + 20 * np.exp(-((days - 2) / 3) ** 2)
        + 15 * np.exp(-((days - ovulation_day) / 2) ** 2)
    )

    data = pd.DataFrame({
        "روز چرخه": days,
        "استروژن": estrogen,
        "پروژسترون": progesterone,
        "LH": lh,
        "FSH": fsh
    })

    st.subheader("تغییرات تقریبی هورمون‌ها")

    st.line_chart(
        data,
        x="روز چرخه",
        y=["استروژن", "پروژسترون", "LH", "FSH"]
    )

    st.caption(
        "این نمودار صرفاً یک مدل آموزشی فرضی است و "
        "غلظت واقعی هورمون‌ها را نشان نمی‌دهد."
    )
    
    st.info(
        "پروژسترون معمولاً پس از تخمک‌گذاری افزایش می‌یابد. "
        "افزایش ناگهانی LH نیز در تحریک تخمک‌گذاری نقش دارد."
    )
elif page == "📚 کتابخانه علمی":

    st.header("📚 کتابخانه علمی CycleLab")

    topic = st.selectbox(
        "موضوع موردنظر را انتخاب کن:",
        [
            "چرخه قاعدگی چیست؟",
            "استروژن",
            "پروژسترون",
            "هورمون LH",
            "هورمون FSH",
            "تخمک‌گذاری"
        ]
    )

    articles = {
        "چرخه قاعدگی چیست؟": """
        چرخه قاعدگی مجموعه‌ای از تغییرات هورمونی و
        فیزیولوژیک است که بدن را برای احتمال بارداری
        آماده می‌کند.
        """,

        "استروژن": """
        استروژن در رشد پوشش داخلی رحم و تنظیم
        چرخه قاعدگی نقش دارد. سطح آن در طول چرخه تغییر می‌کند.
        """,

        "پروژسترون": """
        پروژسترون پس از تخمک‌گذاری، عمدتاً از جسم زرد
        ترشح می‌شود و به آماده نگه داشتن پوشش داخلی رحم کمک می‌کند.
        """,

        "هورمون LH": """
        افزایش ناگهانی LH معمولاً محرک اصلی تخمک‌گذاری است.
        """,

        "هورمون FSH": """
        FSH در رشد و بلوغ فولیکول‌های تخمدان نقش دارد.
        """,

        "تخمک‌گذاری": """
        در تخمک‌گذاری، تخمک از تخمدان آزاد می‌شود.
        زمان آن در همه افراد و همه چرخه‌ها یکسان نیست.
        """
    }

    st.subheader(f"🔬 {topic}")
    st.info(articles[topic])

    st.caption(
        "این مطالب برای آموزش عمومی هستند و جایگزین ارزیابی پزشکی نیستند."
    )   

elif page == "📅 تقویم قاعدگی":

    from streamlit_calendar import calendar
    from datetime import date, timedelta

    st.header("📅 تقویم CycleLab")

    st.write("تقویم آموزشی چرخه قاعدگی خودت را مشاهده کن.")

    last_period = st.date_input(
        "تاریخ شروع آخرین قاعدگی",
        value=date.today(),
        key="calendar_period"
    )

    cycle_length = st.slider(
        "طول چرخه (روز)",
        21, 35, 28,
        key="calendar_length"
    )

    period_duration = st.slider(
        "مدت قاعدگی (روز)",
        2, 10, 5
    )

    events = []

    for cycle in range(4):

        start = last_period + timedelta(
            days=cycle * cycle_length
        )

        # روزهای قاعدگی
        events.append({
            "title": "🩸 قاعدگی تخمینی",
            "start": start.isoformat(),
            "end": (
                start + timedelta(days=period_duration)
            ).isoformat(),
            "backgroundColor": "#e879a9"
        })

        # روز احتمالی تخمک گذاری
        ovulation = start + timedelta(
            days=cycle_length - 14
        )

        events.append({
            "title": "🌸 تخمک گذاری احتمالی",
            "start": ovulation.isoformat(),
            "allDay": True,
            "backgroundColor": "#9b72cf"
        })

    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth"
        },
        "initialView": "dayGridMonth",
        "selectable": False,
        "height": 650
    }

    calendar(
        events=events,
        options=calendar_options,
        key="cycle_calendar"
    )

    st.info(
        "تاریخ‌های این تقویم تخمینی و آموزشی هستند. "
        "زمان واقعی قاعدگی و تخمک‌گذاری ممکن است متفاوت باشد."
    )

elif page == "📝 ثبت علائم روزانه":

    st.header("📝 دفتر ثبت علائم روزانه")
    st.write("علائم روزانه خودت را ثبت کن.")

    import os

    symptom_file = "symptoms.json"

    if os.path.exists(symptom_file):
        with open(symptom_file, "r", encoding="utf-8") as file:
            symptoms = json.load(file)
    else:
        symptoms = []

    with st.form("symptom_form"):

        symptom_date = st.date_input(
            "تاریخ ثبت",
            value=date.today()
        )

        pain = st.select_slider(
            "میزان درد",
            options=["بدون درد", "کم", "متوسط", "زیاد"]
        )

        mood = st.selectbox(
            "وضعیت خلق‌وخو",
            ["خوب", "معمولی", "غمگین", "مضطرب", "تحریک‌پذیر"]
        )

        fatigue = st.selectbox(
            "میزان خستگی",
            ["بدون خستگی", "کم", "متوسط", "زیاد"]
        )

        headache = st.checkbox("سردرد داشتم")

        notes = st.text_area(
            "یادداشت روزانه",
            placeholder="امروز چه احساسی داشتم؟"
        )

        submitted = st.form_submit_button(
            "💗 ذخیره اطلاعات"
        )

    if submitted:

        record = {
            "date": symptom_date.isoformat(),
            "pain": pain,
            "mood": mood,
            "fatigue": fatigue,
            "headache": headache,
            "notes": notes
        }

        symptoms.append(record)

        with open(symptom_file, "w", encoding="utf-8") as file:
            json.dump(
                symptoms,
                file,
                ensure_ascii=False,
                indent=4
            )

        st.success("اطلاعات روزانه ذخیره شد! 🌸")

    st.divider()

    st.subheader("📚 تاریخچه علائم")

    if symptoms:

        for item in reversed(symptoms):

            with st.expander(
                f"📅 {item['date']}"
            ):

                st.write("درد:", item["pain"])
                st.write("خلق‌وخو:", item["mood"])
                st.write("خستگی:", item["fatigue"])
                st.write(
                    "سردرد:",
                    "بله" if item["headache"] else "خیر"
                )
                st.write("یادداشت:", item["notes"])

    else:
        st.info("هنوز اطلاعاتی ثبت نشده است.")
elif page == "🧠 تحلیل هوشمند چرخه":

    st.title("🧠 تحلیل هوشمند چرخه")
    st.write("یک نگاه آموزشی به وضعیت چرخه قاعدگی")

    st.info(
        "این تحلیل بر اساس یک مدل ساده آموزشی است "
        "و جایگزین نظر پزشک یا بررسی پزشکی نیست."
    )

    if "cycle_data.json" in os.listdir():

        with open("cycle_data.json", "r", encoding="utf-8") as file:
            cycle_data = json.load(file)

        cycle_length = cycle_data.get("cycle_length", 28)
        cycle_day = cycle_data.get("cycle_day", 1)

        st.metric("طول چرخه ثبت‌شده", f"{cycle_length} روز")
        st.metric("روز فعلی چرخه", f"{cycle_day}")

        if cycle_day <= 5:
            st.subheader("🩸 مرحله قاعدگی")
            st.write(
                "در این مرحله پوشش داخلی رحم ریزش می‌کند. "
                "سطح استروژن و پروژسترون معمولاً پایین است."
            )

        elif cycle_day < cycle_length - 14:
            st.subheader("🌱 مرحله فولیکولی")
            st.write(
                "فولیکول‌ها در تخمدان رشد می‌کنند و "
                "استروژن معمولاً به‌تدریج افزایش می‌یابد."
            )

        elif cycle_day <= cycle_length - 12:
            st.subheader("🥚 حوالی تخمک‌گذاری")
            st.write(
                "در چرخه‌های معمول، افزایش ناگهانی LH "
                "با فرایند تخمک‌گذاری ارتباط دارد."
            )

        else:
            st.subheader("🌙 مرحله لوتئال")
            st.write(
                "پس از تخمک‌گذاری، پروژسترون معمولاً افزایش می‌یابد "
                "و بدن برای احتمال بارداری آماده می‌شود."
            )

        st.caption(
            "توجه: این مرحله‌بندی فقط تخمینی است؛ "
            "زمان واقعی تخمک‌گذاری و تغییرات هورمونی ممکن است متفاوت باشد."
        )

    else:
        st.warning(
            "هنوز اطلاعات چرخه‌ای ثبت نشده است. "
            "ابتدا اطلاعات چرخه را در صفحه مربوطه وارد کن."
        )
elif page == "📈 داشبورد گرافیکی":

    import numpy as np
    import pandas as pd

    st.title("📈 داشبورد گرافیکی CycleLab")
    st.write("بررسی آموزشی تغییرات هورمون‌ها در طول چرخه")

    cycle_length = st.slider(
        "طول چرخه فرضی را انتخاب کن:",
        min_value=21,
        max_value=35,
        value=28
    )

    days = np.arange(1, cycle_length + 1)

    estrogen = (
        20
        + 65 * np.exp(-((days - (cycle_length * 0.43)) / 4) ** 2)
        + 20 * np.exp(-((days - (cycle_length * 0.85)) / 6) ** 2)
    )

    progesterone = (
        15
        + 70 * np.exp(-((days - (cycle_length * 0.72)) / 5) ** 2)
    )

    lh = (
        10
        + 100 * np.exp(-((days - (cycle_length * 0.5)) / 1.5) ** 2)
    )

    fsh = (
        20
        + 30 * np.exp(-((days - 2) / 3) ** 2)
        + 20 * np.exp(-((days - (cycle_length * 0.5)) / 3) ** 2)
    )

    df = pd.DataFrame({
        "روز چرخه": days,
        "استروژن": estrogen,
        "پروژسترون": progesterone,
        "LH": lh,
        "FSH": fsh
    })

    st.subheader("نمودار تغییرات هورمونی")

    st.line_chart(
        df.set_index("روز چرخه"),
        y=["استروژن", "پروژسترون", "LH", "FSH"]
    )

    st.subheader("🔬 انتخاب هورمون")

    hormone = st.selectbox(
        "کدام هورمون را بررسی کنیم؟",
        ["استروژن", "پروژسترون", "LH", "FSH"]
    )

    st.line_chart(
        df.set_index("روز چرخه")[hormone]
    )

    st.info(
        "این نمودارها داده‌های فرضی و آموزشی هستند؛ "
        "مقادیر آن‌ها آزمایش واقعی یا پیش‌بینی دقیق وضعیت بدن نیستند."
    )      
elif page == "📄 گزارش چرخه":

    import io
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    st.title("📄 گزارش چرخه CycleLab")

    st.write("ساخت یک گزارش ساده از اطلاعات ثبت‌شده")

    if os.path.exists("cycle_data.json"):

        with open("cycle_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        cycle_length = data.get("cycle_length", 28)
        cycle_day = data.get("cycle_day", 1)

        st.subheader("اطلاعات چرخه")

        st.write(f"طول چرخه: {cycle_length} روز")
        st.write(f"روز فعلی چرخه: {cycle_day}")

        if os.path.exists("symptoms.json"):

            with open("symptoms.json", "r", encoding="utf-8") as file:
                symptoms = json.load(file)

            st.write(f"تعداد ثبت علائم: {len(symptoms)}")

        else:
            symptoms = []
            st.write("هنوز علامتی ثبت نشده است.")

        pdf_buffer = io.BytesIO()

        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

        pdf.setFont("Helvetica", 14)

        pdf.drawString(50, 800, "CycleLab - Cycle Report")
        pdf.drawString(50, 760, f"Cycle length: {cycle_length} days")
        pdf.drawString(50, 730, f"Current cycle day: {cycle_day}")
        pdf.drawString(50, 700, f"Symptom records: {len(symptoms)}")

        pdf.drawString(50, 650, "Educational report - Not a medical diagnosis")

        pdf.save()

        pdf_buffer.seek(0)

        st.download_button(
            label="⬇️ دانلود گزارش PDF",
            data=pdf_buffer,
            file_name="CycleLab_Report.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("ابتدا اطلاعات چرخه را ثبت کن.")      
elif page == "💾 پشتیبان‌گیری اطلاعات":

    import json

    st.title("💾 پشتیبان‌گیری اطلاعات")
    st.write("مدیریت فایل‌های اطلاعات CycleLab")

    files = [
        "cycle_data.json",
        "cycle_history.json",
        "symptoms.json"
    ]

    backup_data = {}

    for filename in files:

        if os.path.exists(filename):

            with open(filename, "r", encoding="utf-8") as file:
                backup_data[filename] = json.load(file)

    st.subheader("📦 ساخت نسخه پشتیبان")

    backup_json = json.dumps(
        backup_data,
        ensure_ascii=False,
        indent=4
    )

    st.download_button(
        label="⬇️ دانلود نسخه پشتیبان",
        data=backup_json,
        file_name="CycleLab_Backup.json",
        mime="application/json"
    )

    st.divider()

    st.subheader("📥 بازیابی اطلاعات")

    uploaded_file = st.file_uploader(
        "فایل پشتیبان JSON را انتخاب کن",
        type=["json"]
    )

    if uploaded_file is not None:

        if st.button("بازیابی اطلاعات"):

            try:
                restored_data = json.load(uploaded_file)

                if not isinstance(restored_data, dict):
                    raise ValueError("فرمت فایل معتبر نیست.")

                for filename in files:

                    if filename in restored_data:

                        with open(filename, "w", encoding="utf-8") as file:
                            json.dump(
                                restored_data[filename],
                                file,
                                ensure_ascii=False,
                                indent=4
                            )

                st.success("اطلاعات با موفقیت بازیابی شدند!")
                st.rerun()

            except Exception:
                st.error("فایل انتخاب‌شده معتبر نیست.")        
    # Daily Hormone Analysis

st.divider()

st.header("🔬 تحلیل روزانه چرخه قاعدگی")

cycle_length = st.slider(
    "طول چرخه قاعدگی",
    min_value=21,
    max_value=35,
    value=28,
    key="analysis_cycle_length"
)

cycle_day = st.slider(
    "روز فعلی چرخه",
    min_value=1,
    max_value=cycle_length,
    value=10
)

ovulation_day = cycle_length - 14

if cycle_day <= 5:
    phase = "قاعدگی"
    explanation = """
    پوشش داخلی رحم در حال ریزش است.
    استروژن و پروژسترون معمولاً در سطح پایینی قرار دارند.
    """

elif cycle_day < ovulation_day:
    phase = "مرحله فولیکولی"
    explanation = """
    فولیکول‌های تخمدان در حال رشد هستند.
    استروژن معمولاً افزایش پیدا می‌کند.
    """

elif cycle_day == ovulation_day:
    phase = "زمان احتمالی تخمک‌گذاری"
    explanation = """
    در این حوالی، افزایش ناگهانی LH می‌تواند
    تخمک‌گذاری را تحریک کند.
    """

else:
    phase = "مرحله لوتئال"
    explanation = """
    پس از تخمک‌گذاری، جسم زرد معمولاً پروژسترون تولید می‌کند.
    اگر بارداری رخ ندهد، سطح این هورمون‌ها در ادامه کاهش می‌یابد.
    """

st.subheader(f"🌷 مرحله احتمالی: {phase}")

st.write(explanation)

st.warning(
    "این نتیجه بر اساس یک مدل ساده آموزشی است. "
    "روز دقیق تخمک‌گذاری را نمی‌توان فقط از روی طول چرخه تعیین کرد."
)


# Menstrual Cycle Tracker

st.divider()
st.header("🩸 ثبت و پیگیری چرخه قاعدگی")

st.write(
    "تاریخ شروع آخرین پریود و طول چرخه را وارد کن."
)

with st.form("cycle_form"):

    last_period = st.date_input(
        "تاریخ شروع آخرین پریود",
        value=date.today()
    )

    cycle_length = st.number_input(
        "طول چرخه قاعدگی (روز)",
        min_value=21,
        max_value=35,
        value=28
    )

    submitted = st.form_submit_button(
        "محاسبه و ذخیره اطلاعات"
    )

if submitted:

    next_period = last_period + timedelta(
        days=int(cycle_length)
    )

    cycle_data = {
        "last_period": last_period.isoformat(),
        "cycle_length": int(cycle_length),
        "next_period_estimate": next_period.isoformat()
    }

    with open(
        "cycle_data.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            cycle_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    st.success("اطلاعات با موفقیت ذخیره شد! 🌷")

    st.metric(
        "تاریخ تخمینی پریود بعدی",
        next_period.strftime("%Y-%m-%d")
    )

    st.caption(
        "این تاریخ تقریبی است و ممکن است با تاریخ واقعی متفاوت باشد."
    )

    # Cycle History

st.divider()

st.header("📊 تاریخچه چرخه‌های قاعدگی")

HISTORY_FILE = "cycle_history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


history = load_history()

with st.form("history_form"):
    period_date = st.date_input(
        "تاریخ شروع پریود",
        value=date.today(),
        key="history_period_date"
    )

    length = st.number_input(
        "طول چرخه ثبت‌شده (روز)",
        min_value=1,
        max_value=100,
        value=28,
        key="history_cycle_length"
    )

    save_button = st.form_submit_button("ثبت چرخه")

if save_button:
    record = {
        "start_date": period_date.isoformat(),
        "cycle_length": int(length)
    }

    if not any(
        item["start_date"] == record["start_date"]
        for item in history
    ):
        history.append(record)
        history.sort(key=lambda item: item["start_date"])
        save_history(history)
        st.success("چرخه با موفقیت ثبت شد! 🌷")
        st.rerun()
    else:
        st.warning("این تاریخ قبلاً ثبت شده است.")

if history:
    df = pd.DataFrame(history)
    df["start_date"] = pd.to_datetime(df["start_date"])
    df = df.sort_values("start_date")

    st.subheader("📅 چرخه‌های ثبت‌شده")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 مقایسه طول چرخه‌ها")

    chart_data = df.set_index("start_date")[["cycle_length"]]

    st.line_chart(
        chart_data,
        y="cycle_length",
        x_label="تاریخ شروع چرخه",
        y_label="طول چرخه (روز)"
    )

    if len(df) >= 2:
        average_length = df["cycle_length"].mean()

        st.metric(
            "میانگین طول چرخه‌های ثبت‌شده",
            f"{average_length:.1f} روز"
        )

else:
    st.info("هنوز چرخه‌ای ثبت نشده است. اولین چرخه را اضافه کن.")