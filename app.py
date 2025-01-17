import streamlit as st
import googlemaps
import openpyxl

# ----------------------------------------------------
# 1) הגדרת API Key ויצירת לקוח Google Maps
# ----------------------------------------------------
API_KEY = "AIzaSyBlo9MobgTHKPWnNh8xzLiioQItIRo5CYA"  # הכנס את המפתח התקין שלך מגוגל קלאוד
gmaps = googlemaps.Client(key=API_KEY)

# ----------------------------------------------------
# 2) פונקציות עזר
# ----------------------------------------------------
def get_distance(origin, destination):
    """
    מחזירה מחרוזת של מרחק, למשל '33.2 km'.
    משתמשת ב-distance_matrix של googlemaps.
    """
    res = gmaps.distance_matrix(origins=origin, destinations=destination, mode="driving")
    return res['rows'][0]['elements'][0]['distance']['text']  # 'xx.x km'


def distance_to_float(distance_text):
    """
    הופכת '33.2 km' ל-33.2 (float).
    """
    clean = distance_text.replace("km", "").strip()
    return float(clean)

# ----------------------------------------------------
# 3) כותרת לאפליקציה ועיצוב בסיסי
# ----------------------------------------------------
st.set_page_config(page_title="Distance Calculator", layout="centered")
st.image("PIC.jpg", width=50)

st.title("📍 מחשבון מרחקים - הלוך חזור")
st.markdown("### מחשב מרחק הלוך-חזור בין כתובת מקור ליעדים ומחשב עלות דלק.")

# ----------------------------------------------------
# 4) בחירת מקור
# ----------------------------------------------------
DEFAULT_ORIGIN = "Beit Shemesh Roy Klein 21"

st.sidebar.header("הגדרות מקור")
use_default = st.sidebar.radio("האם להשתמש במקור ברירת המחדל?", ["כן", "לא"], index=0)

if use_default == "כן":
    origin = DEFAULT_ORIGIN
else:
    origin = st.sidebar.text_input("הכנס כתובת מקור חלופית:", value="")

st.sidebar.markdown(f"📍 **כתובת מקור נבחרת:** {origin or '[לא הוזנה]'}")

# ----------------------------------------------------
# 5) קבלת יעדים בבת אחת
# ----------------------------------------------------
st.header("💼 הוספת יעדים")
destinations_str = st.text_area("🔹 הדבק כאן כתובות יעד (מופרדות בפסיק):", "")
destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]

# ----------------------------------------------------
# 6) כפתור 'חשב מרחק הלוך-חזור'
# ----------------------------------------------------
if st.button("📊 חישוב מרחקים"):
    # בדיקות בסיסיות
    if not origin:
        st.warning("❗ לא הוזנה כתובת מקור.")
    elif not destinations:
        st.warning("❗ לא הוזנו יעדים.")
    else:
        # מחשבים מרחק הלוך-חזור לכל יעד
        results = []
        for dest in destinations:
            try:
                going_text = get_distance(origin, dest)
                return_text = get_distance(dest, origin)
                total_num = distance_to_float(going_text) + distance_to_float(return_text)
                total_text = f"{total_num:.2f} km"
                cost_num = total_num * 0.6
                cost_text = f"{cost_num:.2f} ₪"

                # שומר תוצאות
                results.append([dest, total_text, cost_text])

            except Exception as e:
                st.error(f"שגיאה בחישוב המרחק עבור {dest}: {e}")

        # ------------------------------------------------
        # 7) הצגת תוצאות
        # ------------------------------------------------
        if results:
            st.subheader("🔍 תוצאות חישוב")
            for row in results:
                st.write(f"- יעד: **{row[0]}** | מרחק: {row[1]} | עלות: {row[2]}")

            # --------------------------------------------
            # 8) יצוא לאקסל
            # --------------------------------------------
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Distances"
            ws.append(["Destination", "Round Trip Distance", "Cost"])
            for row in results:
                ws.append(row)

            excel_filename = "distances_round_trip.xlsx"
            wb.save(excel_filename)

            # כפתור הורדה של Excel
            with open(excel_filename, "rb") as f:
                excel_data = f.read()
            st.download_button(
                label="📥 הורד קובץ Excel",
                data=excel_data,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
