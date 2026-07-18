import time

import web_search
import web_scrape
import generate_questions
import summarizer
import rag
import headings

def research(
        city: str = '',
        output_file: str = '',
) -> None:
    
    if not city:
        raise ValueError('Input city cannot be empty.')
    if not output_file:
        raise ValueError('Output file cannot be empty.')
    
    print('Generating some queries to search for . . .', end='')
    gen = generate_questions.GenerateQuestions()
    gen.get_questions(city)
    print(f' Generated {len(gen.queries)} queries.')    

    print('Searching for web links . . .', end='')
    ws = web_search.WebSearch()
    ws.get_links(gen.queries)
    all_links = ws.links
    print(f' {len(all_links)} links found.')

    print('Scraping data from web links . . .', end='')
    wsr = web_scrape.WebScrape()
    wsr.scrape(ws.links)
    print(' Done.')

    print('Summarizing collected documents. . .', end='')
    documents = list(wsr.documents.values())
    summ = summarizer.Summarizer()
    summary = summ.summarize(documents)
    print(' Done.')

    print('Building a RAG system and answering generated questions . . .', end='')
    retriever = rag.RAG(documents)
    retriever.answer_questions(gen.queries)
    print(' Done.')

    print('Putting it all together, and writing to output file . . .', end='')
    headings_mapper = headings.Headings()
    headings_mapper.get_headings(gen.queries)
    summary_text = summary.content + '\n\n'
    for q, val in retriever.responses.items():
        if q in headings_mapper.headings_map:
            heading = headings_mapper.headings_map[q]
            summary_text += heading + '\n'
            summary_text += val + '\n\n'

    with open(output_file, 'w') as fptr:
        fptr.write(summary_text)

    print(' Done.')
