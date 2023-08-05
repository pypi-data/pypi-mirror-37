happy_pandas
============

- HBase to Pandas DataFrame conversion

- HBase to Spark DataFrame conversion and vice-versa


### dependencies
- pandas
- happybase
- pyspark

### installation

```
pip install git+ssh://git@code.corp.voyager.ph/jorick.caberio/happy_pandas.git
```

### usage
```python
import happy_pandas
pandas_df = happy_pandas.toDF("localhost", 8080, "recommender_score_card", "verified")
spark_df = happy_pandas.toSparkDF(spark_session,"localhost", 8080, "recommender_score_card", "verified")
happy_pandas.toHB(user_recommendations_df, "localhost", 8080, "recommender_score_card", "artificial_v4")
```

