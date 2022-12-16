# docspace

credits to [nadahlberg](https://devpost.com/nadahlberg) link to his work https://devpost.com/software/docspace

## video
https://youtu.be/6Il_5bYY7NY

## Inspiration
Docspace aims to fill a void in the kind of information that is typically available with legal research products by diving into the text of complaints (and in the future judge orders) and identifying the specific claims, counts, and causes of action relevant to a case.

A little context: The two main reasons the U.S. Federal Court system remains an enigma to legal researchers and practitioners alike are (i) the prohibitively expensive costs associated with purchasing docket sheets and documents from PACER and (ii) the lack of tools needed to convert these documents into the structured data for analysis at scale. Great strides have been make on both fronts. Open access projects like Free Law's RECAP make data acquisition cheaper by crowdsourcing the collection of documents, while products like Lexis Nexis' Lex Machina and Fast Case's Docket Alarm have built out analytics layers that classify key litigation events in a case.

One downside of the products on the analytics side is that they primarily rely only on the text on the face of docket sheets (a special kind of case index that list every document filed in a case, that includes a small paragraph description for each filing). While these descriptions do often contain important infomation, including when a judge takes an action on a party-filed motion, there is insufficient information to achieve the full level of granularity needed to fully understand the lifecycle of a case or aggregate judge behavior. For example, while docket descriptions often show whether a motion to dismiss was granted or denied, the most common outcome is that the motions was granted _ in part _ as to some counts and denied as to others.

In order to really understand judge behavior and litigation pathways _ at the level of individual claims and causes of action _ one must look in the documents. Docspace takes the first step in this direction by demonstrating how large language models can be used to quickly bootstrap a pipeline for extracting, summarizing, and developing an ontology of the specific claims articulated by the plaintiff in a complaint. Future work would apply a similar approach, not only to complaints, but also judge orders, allowing the legal analytics practitioner to collect data on individual claims from their inception to the actions that dispose of them.

## What it does
The tool is simple, you create an account (judge login credentials posted on the login page) and upload a complaint. When you upload the complaint, the following happens:

Step 1: Text is extracted from the pdf and the document is split into chunks.
Step 2: Chunks are filtered using a simple heuristics to identify section likely to include information about the claims, counts, and causes of action being brouckg in the case
Step 3: Using a Cohere model we generate a zero-shot summary of the relevant chunks using two prompts: one to extract the relevant statutes being cited in the chunk, and another to describe those statutes.
Step 4: Also using a Cohere model we generate embeddings for the generated summaries (which tend to be more standardized and less polluted by OCR artifacts compared to the text they were derived from).
Step 5: The summary embeddings are clustered into 100 claim types, and finally, using the most representative examples from each cluster we ask a Cohere model to generate a consolidated summary of the cluster itself.
Step 6: Steps 1-5 have been precomputed and applied to an initial corpus of 400 publicly available complaints. Additionally a FAISS search index has been created for the chunk embeddings of these examples. When a user uploads a new document, their chunk embeddings are queried against this index to find which cluster provisions most likely apply to their document. They are presented with a dashboard for their document which allows them to see the claim types that apply to their case, the generated description of each claim type, the textual evidence from their own document, and a list of similar complaints from the pool of public documents.
How we built it
The dataset was collected using the RECAP API to search CourtListener for documents that included the word complaint in the description. We then used a transformer model by SCALES-OKN (hosted on Hugging Face) to filter the descriptions for documents that were actually complaints. After bulk crawling the PDFs, these were uploaded via the pipeline described above.

The application itself is a Django web application with a PostgreSQL database. The current demo is being served using Digital Ocean cloud services.

The models used for creating embeddings and summaries are by Cohere. Due to time contraints we relied solely on zero-shot prompting, but as is discussed below we beleive big improvements could be made with a bit of annotation and finetuning.

## Challenges we ran into
The intial plan was to substitute the first part of Step 3 above with a NER style model that would extract and itemize specific laws and statutes mentioned in the document chunks. We created initial prototype using only 50 annotations (again with Cohere) and the results were very promising, but needed more annotation labor to be of acceptable quality. Nonetheless, we believe this is a direction worth pursuing in the future, especially because the downstream summaries when you ask for descriptions of a specific law or statue were of incredible high quality.

Step 2 also needs to be replaced by a _ relevant chunk _ classifer. The current heurisitc is far from perfect, likely misses relevant passages, and occasionally extracts chunks of total junk. Furthermore when we apply our summarization to junk entries the model tends to hallucinate a made up description of what is at stake in the case.

## Accomplishments that we're proud of
We are impressed by the quality of the output given the no-training approach in this version of the project. Furthermore getting the application modularized, deployed to production, implementing security and privacy of user uploaded documents, and getting familiar with the Cohere platform in such a short amount of time feels like a big accomplishment.

## What we learned
Zero-shot can go a long way, but finetuning and operationalizing the ability of human reviewers to updated generated content is essential.
Using summarization is an effective way to clean garbled extracted text and to standardize outputs.
Stacking these pipelines can be used to completely automate the first-cut at a litigation ontology.

## What's next for docspace
Implementing the improvements discussed above with finetuned models will greatly improve performance.
There needs to be a more thorough evaluation to ensure that summaries are describing statutes accurately.
Applying a similar pipeline to orders and other court actions so that the claims can be analyzed across the lifecycle of a case.

## Built with
cohere
digitalocean
django
postgresql
python
s3

