from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """ select distinct(Chromosome) from genes where Chromosome!=0"""
        cursor.execute(query)

        results = []

        for row in cursor:
            results.append(row["Chromosome"])

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def getCorrelazione(c1, c2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """ select sum(Expression_Corr) as correlazione from interactions i
                    where GeneID1 in (select distinct(GeneID)from genes where Chromosome = %s)
                    and GeneID2 in (select distinct(GeneID)from genes where Chromosome = %s)"""
        cursor.execute(query, (c1, c2))



        for row in cursor:
            results=(row["correlazione"])

        cursor.close()
        cnx.close()

        return results


