from collections import deque

def explore_agent(site, start, max_pages=4):
    seen, queue = [], deque([start])
    while queue and len(seen) < max_pages:
        url = queue.popleft()
        if url in seen or url not in site:
            continue
        seen.append(url)
        queue.extend(site[url].get('links', []))
    return seen

def observe(site, pages):
    out = {}
    for url in pages:
        text = site[url].get('text', '').lower()
        out[url] = {'title': site[url].get('title', ''), 'words': set(text.split())}
    return out

def evaluate(target, observed):
    target_words = {u: set(p.get('text', '').lower().split()) for u, p in target.items()}
    common = set(target_words) & set(observed)
    page_recall = len(common) / len(target_words) if target_words else 0
    content_scores = []
    for url in common:
        a = target_words[url]
        b = observed[url]['words']
        content_scores.append(len(a & b) / (len(a | b) or 1))
    content = sum(content_scores) / len(content_scores) if content_scores else 0
    score = (page_recall + content) / 2
    return {'page_recall': round(page_recall, 3), 'content_jaccard': round(content, 3), 'score': round(score, 3)}

def main():
    target = {
        '/': {'title': 'Home', 'text': 'AI website reconstruction benchmark browser agent', 'links': ['/about', '/docs']},
        '/about': {'title': 'About', 'text': 'We build browser agents that explore and rebuild websites', 'links': ['/']},
        '/docs': {'title': 'Docs', 'text': 'Benchmark tasks for website reconstruction with agents', 'links': ['/about', '/pricing']},
        '/pricing': {'title': 'Pricing', 'text': 'Open benchmark free tier', 'links': ['/']}
    }
    visited = explore_agent(target, '/', max_pages=3)
    observed = observe(target, visited)
    result = evaluate(target, observed)
    print('Visited pages:', visited)
    print('Reconstruction score:', result)

if __name__ == '__main__':
    main()
