import streamlit as st
import pandas as pd
import datetime

# تنظیمات اولیه صفحه وب
st.set_page_config(page_title="نرم‌افزار جامع حسابداری صنعتی", layout="wide", page_icon="📊")

# استایل‌دهی برای راست‌چین کردن پنل (مناسب زبان فارسی)
st.markdown('''
    <style>
        * { font-family: Tahoma, sans-serif; }
        .stApp { direction: rtl; }
        .stTextInput>div>div>input { text-align: right; }
    </style>
''', unsafe_allow_html=True)

# --- مدیریت نشست (Session State) برای تست رایگان ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'trial_start' not in st.session_state:
    st.session_state.trial_start = None

# تابع صفحه ورود (لاگین)
def login_page():
    st.title("📊 سیستم ابری مدیریت تولید و قیمت‌گذاری")
    st.markdown("### پلتفرم یکپارچه تصمیم‌گیری استراتژیک")
    st.info("برای فعال‌سازی **تست رایگان ۲۴ ساعته**، لطفا شماره موبایل خود را وارد کنید.")
    
    phone = st.text_input("شماره موبایل (مثال: 09121234567)")
    if st.button("🚀 ورود و شروع تست رایگان", use_container_width=True):
        if len(phone) >= 10:
            st.session_state.logged_in = True
            st.session_state.trial_start = datetime.datetime.now()
            st.rerun()
        else:
            st.error("لطفا یک شماره موبایل معتبر وارد کنید.")

# تابع اصلی اپلیکیشن پس از ورود
def main_app():
    # بررسی زمان تست رایگان
    elapsed = datetime.datetime.now() - st.session_state.trial_start
    if elapsed.total_seconds() > 24 * 3600:
        st.error("⛔ مهلت تست ۲۴ ساعته شما به پایان رسیده است. جهت ادامه، نیازمند تهیه اشتراک هستید.")
        st.button("💳 پرداخت و فعال‌سازی اشتراک دائمی")
        st.stop()
    
    remaining_hours = 24 - (elapsed.total_seconds() / 3600)
    
    # منوی کناری (Sidebar)
    st.sidebar.title("منوی مدیریت")
    st.sidebar.success(f"⏳ زمان باقیمانده تست: {remaining_hours:.1f} ساعت")
    
    menu = st.sidebar.radio("بخش‌های سیستم", [
        "📈 داشبورد کلان", 
        "📋 مدیریت BOM استاندارد", 
        "🎯 تحلیل نقطه سر به سر (CVP)"
    ])
    
    # بخش ۱: داشبورد کلان
    if menu == "📈 داشبورد کلان":
        st.header("داشبورد عملکرد مالی و تولید")
        st.markdown("نمای کلی از وضعیت انحرافات و بهای تمام‌شده جهت تصمیم‌گیری سریع تیم مدیریت.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("مجموع تولید (ماه جاری)", "۱,۵۰۰ واحد", "۱۲٪ رشد 🟢")
        col2.metric("انحرافات کل مواد", "-۲,۵۰۰,۰۰۰ ریال", "انحراف نامساعد 🔴")
        col3.metric("میانگین حاشیه سود", "۳۵٪", "۳٪ بهبود 🟢")
        
        st.markdown("### مقایسه بهای استاندارد و واقعی")
        # داده‌های فرضی برای نمودار
        chart_data = pd.DataFrame({
            'بهای استاندارد': [195000, 140000, 250000],
            'بهای واقعی': [205000, 135000, 260000]
        }, index=['محصول آلفا', 'محصول بتا', 'محصول گاما'])
        
        st.bar_chart(chart_data)

    # بخش ۲: مدیریت BOM
    elif menu == "📋 مدیریت BOM استاندارد":
        st.header("مدیریت ساختار محصول (BOM)")
        st.write("ویرایش زنده بهای استاندارد قطعات و مواد مستقیم:")
        
        # جدول قابل ویرایش
        df_bom = pd.DataFrame({
            'کد محصول': ['P-101', 'P-102', 'P-103'],
            'مواد مستقیم (ریال)': [120000, 85000, 150000],
            'دستمزد مستقیم (ریال)': [45000, 35000, 60000],
            'سربار جذب‌شده (ریال)': [30000, 20000, 40000]
        })
        
        edited_df = st.data_editor(df_bom, num_rows="dynamic", use_container_width=True)
        
        # محاسبات خودکار بهای تمام شده
        edited_df['بهای کل استاندارد'] = edited_df['مواد مستقیم (ریال)'] + edited_df['دستمزد مستقیم (ریال)'] + edited_df['سربار جذب‌شده (ریال)']
        
        st.markdown("### نتیجه نهایی ارزیابی سیستم:")
        st.dataframe(edited_df[['کد محصول', 'بهای کل استاندارد']], use_container_width=True)

    # بخش ۳: تحلیل نقطه سر به سر
    elif menu == "🎯 تحلیل نقطه سر به سر (CVP)":
        st.header("ماشین حساب استراتژیک نقطه سر به سر")
        st.write("ابزار ارزیابی استراتژی‌های فروش با تغییر متغیرهای قیمت و هزینه‌ها.")
        
        col1, col2 = st.columns(2)
        with col1:
            price = st.number_input("قیمت فروش واحد (ریال)", min_value=1000, value=250000, step=10000)
            var_cost = st.number_input("هزینه متغیر واحد (ریال)", min_value=1000, value=150000, step=10000)
        with col2:
            fixed_cost = st.number_input("هزینه ثابت دوره‌ای (ریال)", min_value=10000, value=50000000, step=1000000)
        
        if price > var_cost:
            cm = price - var_cost
            bep = fixed_cost / cm
            margin_pct = (cm / price) * 100
            
            st.success(f"**تارگت سر به سر:** برای پوشش کامل هزینه‌ها، باید حداقل **{bep:,.0f} واحد** تولید و فروخته شود.")
            st.info(f"**حاشیه فروش واحد:** {cm:,.0f} ریال (حاشیه سود ناخالص: {margin_pct:.1f}٪)")
        else:
            st.error("خطای قیمت‌گذاری: قیمت فروش نمی‌تواند از هزینه متغیر کمتر باشد!")

# اجرای منطق برنامه
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
