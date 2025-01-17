import streamlit as st
import googlemaps
import pandas as pd

# ----------------------------------------------------
# 1) הגדרת API Key ויצירת לקוח Google Maps
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
# 2) הגדרות אפליקציה
# ----------------------------------------------------
st.set_page_config(page_title="Distance Calculator", layout="centered")
st.image("image.png", width=200)
st.title("מחשבון מרחקים - הלוך חזור")

# ----------------------------------------------------
# 3) הגדרות מקור
# ----------------------------------------------------
DEFAULT_ORIGIN = "Beit Shemesh Roy Klein 21"

st.markdown("### הוספת יעדים")
destinations_str = st.text_area("הדבק כאן כתובות יעד (מופרדות בפסיק):", "")
destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]

# ----------------------------------------------------
# 4) יצירת טבלה לעריכה
# ----------------------------------------------------
if destinations:
    st.markdown("### עריכת מקור עבור כל יעד")
    data = {
        "יעד": destinations,
        "כתובת מקור": [DEFAULT_ORIGIN] * len(destinations),  # ברירת מחדל
        "שנה מקור": ["" for _ in destinations]  # שדה לעריכה ידנית
    }
    df = pd.DataFrame(data)

    # טבלה אינטראקטיבית לעריכה
    edited_df = st.experimental_data_editor(df, use_container_width=True)

    # ------------------------------------------------
    # 5) חישוב מרחקים
    # ------------------------------------------------
    if st.button("📊 חישוב מרחקים"):
        results = []
        for index, row in edited_df.iterrows():
            # אם כתובת "שנה מקור" לא ריקה, נשתמש בה במקום בברירת המחדל
            origin = row["כתובת מקור"] if not row["שנה מקור"] else row["שנה מקור"]
            destination = row["יעד"]

            try:
                # חישוב הלוך וחזור
                going_text = get_distance(origin, destination)
                return_text = get_distance(destination, origin)
                total_distance = distance_to_float(going_text) + distance_to_float(return_text)
                total_cost = total_distance * 0.6

                # שמירה בתוצאות
                results.append([destination, total_distance, total_cost])

            except Exception as e:
                st.error(f"שגיאה בחישוב המרחק עבור {destination}: {e}")

        # ------------------------------------------------
        # 6) הצגת תוצאות
        # ------------------------------------------------
        if results:
            st.markdown("### תוצאות חישוב:")
            for result in results:
                st.write(f"יעד: {result[0]} | מרחק: {result[1]:.2f} ק\"מ | עלות: {result[2]:.2f} ₪")

            # יצירת DataFrame לתוצאות
            df_results = pd.DataFrame(results, columns=["יעד", "מרחק הלוך-חזור (ק\"מ)", "עלות (ש\"ח)"])

            # כפתור להורדת Excel
            st.download_button(
                label="📥 הורד קובץ Excel",
                data=df_results.to_csv(index=False).encode('utf-8'),
                file_name="distances_round_trip.csv",
                mime="text/csv"
            )
