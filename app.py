import streamlit as st
import googlemaps
import openpyxl
import pandas as pd

# ----------------------------------------------------
# הגדרת API Key ויצירת לקוח Google Maps
# ----------------------------------------------------
API_KEY = "import streamlit as st
import googlemaps
import openpyxl
import pandas as pd

# ----------------------------------------------------
# הגדרת API Key ויצירת לקוח Google Maps
# ----------------------------------------------------
API_KEY = "AIzaSyBlo9MobgTHKPWnNh8xzLiioQItIRo5CYA"  # הכנס את המפתח התקין שלך מגוגל קלאוד
gmaps = googlemaps.Client(key=API_KEY)

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
# כותרת ראשית
# ----------------------------------------------------
st.set_page_config(page_title="Distance Calculator", layout="centered")
st.title("מחשבון מרחקים - הלוך חזור")

# ----------------------------------------------------
# בחירת מקור
# ----------------------------------------------------
DEFAULT_ORIGIN = "Beit Shemesh Roy Klein 21"

st.markdown("### בחר כתובת מקור:")
use_default = st.radio("האם להשתמש במקור ברירת המחדל?", ["כן", "לא"], index=0)

if use_default == "כן":
    origin = DEFAULT_ORIGIN
else:
    origin = st.text_input("הכנס כתובת מקור חלופית:", value="")

st.write(f"**כתובת מקור נבחרת:** {origin or '[לא הוזנה]'}")

# ----------------------------------------------------
# קבלת היעדים בבת אחת
# ----------------------------------------------------
st.markdown("### הוספת יעדים")
destinations_str = st.text_area("הדבק כאן כתובות יעד (מופרדות בפסיק):", "")
destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]

if destinations:
    # ------------------------------------------------
    # טבלה אינטראקטיבית לעריכת המקור והחזרה
    # ------------------------------------------------
    data = {
        "מקור": [DEFAULT_ORIGIN] * len(destinations),
        "יעד": destinations,
        "חזרה לכתובת": [DEFAULT_ORIGIN] * len(destinations)
    }
    df = pd.DataFrame(data)

    st.markdown("### טבלה לעריכה")
    edited_df = st.experimental_data_editor(df, use_container_width=True)

    # ------------------------------------------------
    # כפתור חישוב מחדש
    # ------------------------------------------------
    if st.button("📊 חישוב מרחקים"):
        results = []
        for index, row in edited_df.iterrows():
            origin = row["מקור"]
            destination = row["יעד"]
            return_address = row["חזרה לכתובת"]

            try:
                # חישוב הלוך וחזור
                going_text = get_distance(origin, destination)
                return_text = get_distance(destination, return_address)
                total_distance = distance_to_float(going_text) + distance_to_float(return_text)
                total_cost = total_distance * 0.6

                results.append([destination, total_distance, total_cost])

            except Exception as e:
                st.error(f"שגיאה בחישוב המרחק עבור {destination}: {e}")

        # ------------------------------------------------
        # הצגת תוצאות
        # ------------------------------------------------
        if results:
            st.markdown("### תוצאות חישוב:")
            for result in results:
                st.write(f"יעד: {result[0]} | מרחק: {result[1]:.2f} ק"מ | עלות: {result[2]:.2f} ₪")

            # יצוא לאקסל
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Distances"
            ws.append(["Destination", "Round Trip Distance", "Cost (ILS)"])
            for result in results:
                ws.append(result)

            excel_filename = "distances_round_trip.xlsx"
            wb.save(excel_filename)

            # כפתור הורדה
            with open(excel_filename, "rb") as f:
                excel_data = f.read()
            st.download_button(
                label="📥 הורד קובץ Excel",
                data=excel_data,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
"  # הכנס את המפתח התקין שלך מגוגל קלאוד
gmaps = googlemaps.Client(key=API_KEY)

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
# כותרת ראשית
# ----------------------------------------------------
st.set_page_config(page_title="Distance Calculator", layout="centered")
st.title("מחשבון מרחקים - הלוך חזור")

# ----------------------------------------------------
# בחירת מקור
# ----------------------------------------------------
DEFAULT_ORIGIN = "Beit Shemesh Roy Klein 21"

st.markdown("### בחר כתובת מקור:")
use_default = st.radio("האם להשתמש במקור ברירת המחדל?", ["כן", "לא"], index=0)

if use_default == "כן":
    origin = DEFAULT_ORIGIN
else:
    origin = st.text_input("הכנס כתובת מקור חלופית:", value="")

st.write(f"**כתובת מקור נבחרת:** {origin or '[לא הוזנה]'}")

# ----------------------------------------------------
# קבלת היעדים בבת אחת
# ----------------------------------------------------
st.markdown("### הוספת יעדים")
destinations_str = st.text_area("הדבק כאן כתובות יעד (מופרדות בפסיק):", "")
destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]

if destinations:
    # ------------------------------------------------
    # טבלה אינטראקטיבית לעריכת המקור והחזרה
    # ------------------------------------------------
    data = {
        "מקור": [DEFAULT_ORIGIN] * len(destinations),
        "יעד": destinations,
        "חזרה לכתובת": [DEFAULT_ORIGIN] * len(destinations)
    }
    df = pd.DataFrame(data)

    st.markdown("### טבלה לעריכה")
    edited_df = st.experimental_data_editor(df, use_container_width=True)

    # ------------------------------------------------
    # כפתור חישוב מחדש
    # ------------------------------------------------
    if st.button("📊 חישוב מרחקים"):
        results = []
        for index, row in edited_df.iterrows():
            origin = row["מקור"]
            destination = row["יעד"]
            return_address = row["חזרה לכתובת"]

            try:
                # חישוב הלוך וחזור
                going_text = get_distance(origin, destination)
                return_text = get_distance(destination, return_address)
                total_distance = distance_to_float(going_text) + distance_to_float(return_text)
                total_cost = total_distance * 0.6

                results.append([destination, total_distance, total_cost])

            except Exception as e:
                st.error(f"שגיאה בחישוב המרחק עבור {destination}: {e}")

        # ------------------------------------------------
        # הצגת תוצאות
        # ------------------------------------------------
        if results:
            st.markdown("### תוצאות חישוב:")
            for result in results:
                st.write(f"יעד: {result[0]} | מרחק: {result[1]:.2f} ק"מ | עלות: {result[2]:.2f} ₪")

            # יצוא לאקסל
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Distances"
            ws.append(["Destination", "Round Trip Distance", "Cost (ILS)"])
            for result in results:
                ws.append(result)

            excel_filename = "distances_round_trip.xlsx"
            wb.save(excel_filename)

            # כפתור הורדה
            with open(excel_filename, "rb") as f:
                excel_data = f.read()
            st.download_button(
                label="📥 הורד קובץ Excel",
                data=excel_data,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
