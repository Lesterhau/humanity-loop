"""Fixture latency guidance: preserve upstream role instructions and context."""
GUIDANCE={
    'assign': 'Return three concise bullets, at most 55 words total: responsible reviewer and permitted task; primary-source/date/hash provenance requirements; explicit stop and separate human review. Do not add authorization.',
    'build_act': 'Return the actual reviewable checklist draft, at most 90 words. Include concrete observable checks, required evidence and explicit uncertainties. No claim of completed checks.',
    'dissent': 'At most 75 words: fatal flaws, potentially harmed groups, a falsification test and unknowns. Do not omit a material concern to meet the word target.',
    'revision': 'At most 90 words: revise the concrete draft to address all material dissent and safety conditions. Preserve human review and scope limits.',
    'outcome': 'At most 70 words: what a separate human checks, evidence freshness and closure criteria. Do not claim a real outcome.',
}
def compact_prompt(stage,prompt):
    if stage not in GUIDANCE or not isinstance(prompt,str) or not prompt.strip():
        raise ValueError('invalid_compact_prompt')
    result=prompt+'\nOUTPUT LENGTH GUIDANCE ONLY: '+GUIDANCE[stage]+' Use direct language; no preamble. All original requirements and safety rules remain binding; do not omit material limitations for brevity.'
    if len(result)>12000:
        raise ValueError('prompt_budget_exceeded')
    return result
