#### Los datos extraidos van a ser guardados de dos maneras diferentes para facilitar las tareas que quiero realizar sobre ellos.

1) Los datos en bruto como fueron extraidos del sitio seran guardados en una base de datos relacional usando sqlite3. El analisis exploratorio y descriptivo junto con la evaluacion de data types y algunas tareas de data wranglin se van a apoya en primera instania en esta base de datos.
2) En segundo lugar y para implementar algunas tareas de clustering y analisis de interelaciones estoy planificando implementar dos bases de datos diferentes, no relacionales. Mongo DB y Neo4J ambas bases tambien con propositos diferentes. Neo4J se auto identificand como un motor de bases de datos bueno para el analisis de relacion entre nodos, por su principal caracteristica, bases de datos basadas en grafos. Por otro lado Mongo siendo una base de datos rapida y desestructurada la veo potencial herramienta para alimentar a Neo4J en todo lo relacionado a las caracteristicas de los nodos.
