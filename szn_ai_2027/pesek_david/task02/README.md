# analýzu následujícího problému:
 máte
agentní systém (chatbota), se kterým konverzují uživatelé (řádově miliony unikátních uživatelů,
miliony konverzací denně). Chcete implementovat nějakou formu personalizace, tedy uzpůsobovat
vedení konverzace a jednotlivé odpovědi preferencím uživatele. Navrhněte:
• jaká data potřebujete
• jak je budete zpracovávat a uchovávat
• jak je budete využívat při generování odpovědí
• jak vyhodnotíte, zda jsou výsledky lepší než bez personalizace

# Jaká data potřebuji

## Explicitní (uživatel je zadá vědomě)
- nastavení: styl a délka odpovědí, hlas, jazyk, custom instructions
- přímé pokyny v konverzaci: „zapamatuj si…“, „odpovídej stručněji“
- zpětná vazba: palec nahoru/dolů, výběr mezi dvěma odpověďmi

## Implicitní (systém je odvodí)
- obsah konverzací: fakta o uživateli (povolání, projekty, dieta), témata, styl psaní
- chování: regenerace odpovědi, přeformulování dotazu, opravy, zkopírování odpovědi, opuštění konverzace

## Kontext
- jazyk, země odvozená z IP (samotnou IP neukládám), čas, zařízení
- explicitní nastavení má přednost před odvozeným kontextem

Citlivé kategorie (zdraví, politika…) neukládám bez výslovného souhlasu; uživatel může paměť zobrazit, upravit a smazat (GDPR).

# Zpracování a uchování
1. Po konverzaci (asynchronně přes frontu) malý LLM extrahuje fakta, preference a shrnutí konverzace.
2. Sloučení s existující pamětí: přidat / aktualizovat / smazat / nic (inspirováno Mem0). Novější a explicitní údaj vyhrává.
3. Uložení:
   - **profil** (krátká fakta a preference, ~500 tokenů) → key-value DB podle `user_id`
   - **shrnutí konverzací a detailnější fakta** → embedding → vektorová DB (+ `user_id`, čas, `conversation_id`)
   - **celé konverzace** → historie chatu, neembedují se, dostupné podle ID

# Využití při generování
- **Vždy v system promptu:** profil + krátká shrnutí 3–5 posledních konverzací (podobně jako ChatGPT podle neoficiálních analýz), pevný rozpočet ~1–2k tokenů
- **Na vyžádání:** RAG jako nástroj agenta `search_memory(query)`. Model ho volá, když usoudí, že je potřeba starší kontext, nejen na výslovný dotaz uživatele.
- Pokyn v aktuální konverzaci má přednost před pamětí.
co

lora??
