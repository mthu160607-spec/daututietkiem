import streamlit as st
st.image("IMG_0970.png")
from decimal import Decimal, ROUND_HALF_UP

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    amount = Decimal(str(amount)).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Nhập thông tin tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

st.divider()

# =========================
# NHẬP DỮ LIỆU
# =========================

so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0,
    value=100_000_000,
    step=1_000_000,
    format="%d"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.01,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Tổng tiền lãi trong toàn bộ kỳ hạn
    # Công thức: Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12
    tong_tien_lai = (
        so_tien_gui
        * lai_suat_nam
        * ky_han
        / 12
    )

    # =========================
    # LÃI THEO HÌNH THỨC NHẬN
    # =========================

    if hinh_thuc == "Cuối kỳ":

        so_ky_nhan_lai = 1
        tien_lai_dinh_ky = tong_tien_lai
        mo_ta = f"Nhận toàn bộ tiền lãi sau {ky_han} tháng."

    elif hinh_thuc == "Hàng tháng":

        so_ky_nhan_lai = ky_han
        tien_lai_dinh_ky = tong_tien_lai / ky_han
        mo_ta = "Tiền lãi được nhận mỗi tháng."

    else:  # Hàng quý

        so_ky_nhan_lai = ky_han / 3
        tien_lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai
        mo_ta = "Tiền lãi được nhận mỗi 3 tháng."

    # Tổng tiền gốc + lãi
    tong_nhan_duoc = so_tien_gui + tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.success("✅ ĐÃ TÍNH XONG!")

    st.subheader("📊 KẾT QUẢ")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Tiền lãi định kỳ",
            format_money(tien_lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "💵 Tiền gốc",
            format_money(so_tien_gui)
        )

    with col4:
        st.metric(
            "🏦 Tổng tiền nhận được",
            format_money(tong_nhan_duoc)
        )

    st.info(mo_ta)

    # =========================
    # CHI TIẾT TÍNH TOÁN
    # =========================

    st.subheader("📝 Chi tiết")

    st.write(f"**Số tiền gửi:** {format_money(so_tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

    st.write("---")

    st.write(
        f"**Tổng tiền lãi:** "
        f"{format_money(tong_tien_lai)}"
    )

    st.write(
        f"**Tổng tiền gốc + lãi:** "
        f"{format_money(tong_nhan_duoc)}"
    )

    # =========================
    # BẢNG LỊCH NHẬN LÃI
    # =========================

    if hinh_thuc != "Cuối kỳ":

        st.subheader("📅 Lịch nhận lãi")

        if hinh_thuc == "Hàng tháng":
            so_lan = ky_han
            chu_ky = "Tháng"

        else:
            so_lan = int(ky_han // 3)
            chu_ky = "Quý"

        for i in range(1, so_lan + 1):

            if hinh_thuc == "Hàng tháng":
                thoi_diem = f"Tháng {i}"
            else:
                thoi_diem = f"Quý {i}"

            st.write(
                f"**{thoi_diem}:** "
                f"{format_money(tien_lai_dinh_ky)}"
            )

    else:

        st.subheader("📅 Thời điểm nhận lãi")

        st.write(
            f"Sau {ky_han} tháng: "
            f"**{format_money(tong_tien_lai)}**"
        )


# =========================
# GHI CHÚ
# =========================

st.divider()

st.caption(
    "Lưu ý: Công cụ sử dụng công thức lãi đơn trên tiền gốc. "
    "Kết quả thực tế tại ngân hàng có thể khác do quy định về "
    "ngày tính lãi, cách làm tròn và sản phẩm tiền gửi."
)
