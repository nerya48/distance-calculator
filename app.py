import streamlit as st
import googlemaps
import openpyxl
import pandas as pd

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
st.image("PIC.jpg", width=100)

st.title("💖מחשבון עלות נסיעה -לשירה שלי")
st.markdown("### מחשב מרחק הלוך-חזור בין כתובת מקור ליעדים ומחשב עלות דלק.")

# ----------------------------------------------------
# 4) בחירת מקור
# ----------------------------------------------------
st.header("🏠 הגדרת כתובת מקור")
DEFAULT_ORIGIN = "בית שמש רועי קלין 21"

use_default_global = st.radio("האם להשתמש בכתובת ברירת המחדל?", ["כן", "לא"], index=0)

if use_default_global == "כן":
    global_origin = DEFAULT_ORIGIN
else:
    global_origin = st.text_input("🔹 הכנס כתובת מקור חלופית:", value="")

st.markdown(f"📍 **כתובת מקור נבחרת:** {global_origin or '[לא הוזנה]'}")

# ----------------------------------------------------
# 5) קבלת יעדים והגדרת כתובת מקור וחזרה
# ----------------------------------------------------
st.header("💼 הוספת יעדים")
destinations_str = st.text_area("🔹 הדבק כאן כתובות יעד (מופרדות בפסיק):", "")
destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]

if destinations:
    st.markdown("### עריכת כתובות עבור כל יעד")
    updated_destinations = []

    for i, destination in enumerate(destinations):
        st.markdown(f"**יעד {i + 1}: {destination}**")

        # עריכת כתובת היציאה
        use_default_origin = st.radio(
            f"כתובת ברירת המחדל ליציאה  {destination}?",
            ["כן", "לא"],
            index=0,
            key=f"origin_radio_{i}"
        )

        if use_default_origin == "כן":
            origin = global_origin
        else:
            origin = st.text_input(
                f"🔹 הכנס כתובת יציאה עבור {destination}:",
                key=f"custom_origin_{i}"
            )

        # עריכת כתובת החזרה
        use_default_return = st.radio(
            f"כתובת ברירת המחדל לחזרה  {destination}?",
            ["כן", "לא"],
            index=0,
            key=f"return_radio_{i}"
        )

        if use_default_return == "כן":
            return_address = global_origin
        else:
            return_address = st.text_input(
                f"🔹 הכנס כתובת חזרה עבור {destination}:",
                key=f"custom_return_{i}"
            )

        # הוספת התוצאה לנתונים המעודכנים
        updated_destinations.append({
            "יעד": destination,
            "כתובת יציאה": origin,
            "כתובת חזרה": return_address
        })

    # המרה ל-DataFrame
    df = pd.DataFrame(updated_destinations)

    # הצגת טבלה מעודכנת
    st.subheader("📋 טבלת נתונים מעודכנת")
    st.dataframe(df, use_container_width=True)

# ----------------------------------------------------
# 6) כפתור 'חשב מרחקים'
# ----------------------------------------------------
if st.button("📊 חישוב מרחקים") and destinations:
    results = []
    for i, row in df.iterrows():
        try:
            # שימוש בכתובות היציאה והחזרה המעודכנות מהטבלה
            current_origin = row["כתובת יציאה"]
            current_return = row["כתובת חזרה"]
            destination = row["יעד"]

            # חישוב הלוך וחזור
            going_text = get_distance(current_origin, destination)
            return_text = get_distance(destination, current_return)
            total_num = distance_to_float(going_text) + distance_to_float(return_text)
            total_text = f"{total_num:.2f} km"
            cost_num = total_num * 0.6
            cost_text = f"{cost_num:.2f} ₪"

            # שומר תוצאות
            results.append([destination, total_text, cost_text])

        except Exception as e:
            st.error(f"שגיאה בחישוב המרחק עבור {destination}: {e}")

    # הצגת תוצאות
    if results:
        st.subheader("🔍 תוצאות חישוב")
        for row in results:
            st.write(f"- יעד: **{row[0]}** | מרחק: {row[1]} | עלות: {row[2]}")

        # יצוא לאקסל
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
