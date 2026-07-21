import streamlit as st
import pandas as pd
import datetime

# تنظیمات اولیه صفحه وب
st.set_page_config(page_title="نرم‌افزار جامع حسابداری و مدیریت صنعتی", layout="wide", page_icon="📊")

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
        "🎯 تحلیل نقطه سر به سر (CVP)",
        "📊 تحلیل انحرافات (Variance)",
        "📦 مدیریت انبار و موجودی",
        "🛒 ثبت و پیگیری سفارشات"
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
        chart_data = pd.DataFrame({
            'بهای استاندارد': [195000, 140000, 250000],
            'بهای واقعی': [205000, 135000, 260000]
        }, index=['محصول آلفا', 'محصول بتا', 'محصول گاما'])
        
        st.bar_chart(chart_data)

    # بخش ۲: مدیریت BOM
    elif menu == "📋 مدیریت BOM استاندارد":
        st.header("مدیریت ساختار محصول (BOM)")
        st.write("ویرایش زنده بهای استاندارد قطعات و مواد مستقیم:")
        
        df_bom = pd.DataFrame({
            'کد محصول': ['P-101', 'P-102', 'P-103'],
            'مواد مستقیم (ریال)': [120000, 85000, 150000],
            'دستمزد مستقیم (ریال)': [45000, 35000, 60000],
            'سربار جذب‌شده (ریال)': [30000, 20000, 40000]
        })
        
        edited_df = st.data_editor(df_bom, num_rows="dynamic", use_container_width=True)
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

    # بخش ۴: تحلیل انحرافات
    elif menu == "📊 تحلیل انحرافات (Variance)":
        st.header("تحلیل انحرافات مواد مستقیم و دستمزد")
        st.markdown("ارزیابی انحرافات نرخ و مصرف جهت کنترل دقیق بهای تمام‌شده.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("انحرافات مواد مستقیم")
            std_price_m = st.number_input("نرخ استاندارد مواد (ریال)", value=50000, step=1000)
            act_price_m = st.number_input("نرخ واقعی مواد (ریال)", value=55000, step=1000)
            std_qty_m = st.number_input("مقدار استاندارد مصرف", value=100, step=5)
            act_qty_m = st.number_input("مقدار واقعی مصرف", value=110, step=5)
            
            price_variance = (act_price_m - std_price_m) * act_qty_m
            qty_variance = (act_qty_m - std_qty_m) * std_price_m
            total_mat_variance = price_variance + qty_variance
            
            st.write(f"🔹 انحراف نرخ مواد: **{price_variance:,.0f} ریال**")
            st.write(f"🔹 انحراف مصرف مواد: **{qty_variance:,.0f} ریال**")
            st.error(f"🔴 انحراف کل مواد: **{total_mat_variance:,.0f} ریال** (نامساعد)")

        with col2:
            st.subheader("شاخص‌های کلیدی عملکرد (KPI)")
            st.info("نکات مدیریتی:")
            st.markdown("""
            * **انحراف نرخ نامساعد:** ناشی از تورم بازار یا تغییر تامین‌کننده.
            * **انحراف مصرف نامساعد:** ناشی از ضایعات بالای کارگاهی یا خطای اپراتور.
            * **اقدام اصلاحی:** بازنگری در قراردادهای خرید و کنترل کیفی ایستگاه‌های کاری.
            """)

    # بخش ۵: مدیریت انبار و موجودی
    elif menu == "📦 مدیریت انبار و موجودی":
        st.header("سیستم مدیریت موجودی و انبار مواد اولیه")
        st.markdown("پایش زنده موجودی انبار، ارزیابی ریالی و هشدارهای کمبود مواد.")
        
        df_inventory = pd.DataFrame({
            'کد قطعه': ['M-01', 'M-02', 'M-03', 'M-04'],
            'نام مواد اولیه': ['ورق فولادی', 'مفتول مس', 'قطعات پلیمری', 'رنگ صنعتی'],
            'موجودی فعلی': [120, 45, 300, 15],
            'حداقل ایمنی': [50, 60, 100, 20],
            'ارزش هر واحد (ریال)': [250000, 180000, 45000, 90000]
        })
        
        edited_inv = st.data_editor(df_inventory, num_rows="dynamic", use_container_width=True)
        edited_inv['ارزش کل موجودی (ریال)'] = edited_inv['موجودی فعلی'] * edited_inv['ارزش هر واحد (ریال)']
        
        st.markdown("### وضعیت هشدار و ارزش انبار:")
        total_inv_value = edited_inv['ارزش کل موجودی (ریال)'].sum()
        st.metric("ارزش کل موجودی انبار", f"{total_inv_value:,.0f} ریال")
        
        low_stock = edited_inv[edited_inv['موجودی فعلی'] < edited_inv['حداقل ایمنی']]
        if not low_stock.empty:
            st.warning("⚠️ اقلام زیر به کمتر از حد نصاب ایمنی رسیده‌اند و نیازمند سفارش خرید فوری هستند:")
            st.dataframe(low_stock[['کد قطعه', 'نام مواد اولیه', 'موجودی فعلی', 'حداقل ایمنی']], use_container_width=True)
        else:
            st.success("✅ تمامی اقلام انبار در سطح ایمنی مطلوب قرار دارند.")

    # بخش ۶: ثبت و پیگیری سفارشات
    elif menu == "🛒 ثبت و پیگیری سفارشات":
        st.header("مدیریت ثبت سفارشات مشتریان و خط تولید")
        st.markdown("ثبت سفارش جدید، محاسبه پیش‌بینی درآمد و وضعیت تحویل.")
        
        with st.form("order_form"):
            st.subheader("فرم ثبت سفارش جدید")
            col_a, col_b = st.columns(2)
            with col_a:
                customer_name = st.text_input("نام مشتری / شرکت")
                product_selected = st.selectbox("انتخاب محصول", ["محصول آلفا", "محصول بتا", "محصول گاما"])
            with col_b:
                quantity_ordered = st.number_input("تعداد درخواستی", min_value=1, value=50, step=10)
                delivery_date = st.date_input("تاریخ تحویل مورد انتظار")
            
            submitted = st.form_submit_button("💾 ثبت نهایی سفارش در سیستم")
            if submitted:
                if customer_name:
                    prices = {"محصول آلفا": 250000, "محصول بتا": 180000, "محصول گاما": 320000}
                    total_price = quantity_ordered * prices.get(product_selected, 200000)
                    st.success(f"سفارش برای مشتری **{customer_name}** با موفقیت ثبت شد!")
                    st.info(f"مبلغ کل فاکتور: **{total_price:,.0f} ریال** | وضعیت: در صف تولید 🏭")
                else:
                    st.error("لطفا نام مشتری را وارد کنید.")
        
        st.markdown("### لیست سفارشات جاری در سیستم:")
        df_orders = pd.DataFrame({
            'کد سفارش': ['ORD-101', 'ORD-102'],
            'مشتری': ['صنایع خودرویی پارس', 'تجهیزات الکترونیک نوین'],
            'محصول': ['محصول آلفا', 'محصول بتا'],
            'تعداد': [100, 250],
            'وضعیت': ['در حال تولید ⚙️', 'آماده ارسال 📦']
        })
        st.dataframe(df_orders, use_container_width=True)

# اجرای منطق برنامه
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
