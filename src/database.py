# import mysql.connector
# from mysql.connector import Error

# def get_db_connection():
#     """
#     Établit une connexion avec la base de données MySQL.
#     Utilise les identifiants configurés dans le fichier docker-compose.
#     """
#     try:
#         connection = mysql.connector.connect(
#             host='db',
#             database='socialmetrics_db',
#             user='user_api',
#             password='api_password',
#             port=3306
#         )
#         if connection.is_connected():
#             return connection
#     except Error as e:
#         print(f"Erreur lors de la connexion à MySQL : {e}")
#         return None

# if __name__ == "__main__":
#     conn = get_db_connection()
#     if conn:
#         print("🚀 Connexion réussie à la base de données socialmetrics_db !")
#         conn.close()
#     else:
#         print("❌ Échec de la connexion.")
