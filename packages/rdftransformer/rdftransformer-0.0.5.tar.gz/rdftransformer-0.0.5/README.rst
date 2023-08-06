<h1>rdftransformer Module Repository</h1>

<p>
This project is intendet to annotate data according to the ALKIS Ontology.

Additionally it is desired for the tool to be generic.
</p>


<h2>Getting Started</h2>

<p>
Given that 'ontology.owl' and 'data.xml' directories are known: 

<ol>
<li>Importing the ontology with a preferred prefix. For alkis it would be <b>alk</b>.</li>
<li>Importing the data to transform.</li>
<li>Getting the desired elements from the data.xml.</li>
<li>Looping through the elements and transforming them.</li>
<li>Outputting the transformed data to console or file.</li>
</ol>

<p>Example Code:</p>
<pre><code>
from rdftransformer import Annotation

a = Annotation()
a.importOntology("ontology.owl", "ontologyPrefix")
a.importData("data.xml")

elements = a.getElementsByTagName("elementName", "parentName")
for element in elements:
	a.annotate(element)

a.output()
</code></pre>
</p>