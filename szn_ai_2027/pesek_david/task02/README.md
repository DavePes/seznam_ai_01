# Personalizace chatbota - implementační analýza

## Zadání
Agentní systém (chatbot) s řádově miliony unikátních uživatelů a miliony konverzací denně. Cílem je přizpůsobit vedení konverzace i jednotlivé odpovědi preferencím uživatele. Analýza pokrývá: jaká data potřebujeme, jak je zpracujeme a uchováme, jak je využijeme při generování a jak vyhodnotíme, zda jsou výsledky lepší než bez personalizace.

## 1. Jaká data potřebujeme
Rozdělení vychází z taxonomie v [1] (lehce upravené pro náš případ).

**Explicitní (uživatel je zadá vědomě)**
- nastavení: styl a délka odpovědí, hlas, jazyk, custom instructions
- přímé pokyny v konverzaci: „zapamatuj si…“, „odpovídej stručněji“
- zpětná vazba: palec nahoru/dolů, výběr mezi dvěma odpověďmi

**Implicitní (systém je odvodí)**
- obsah konverzací: fakta o uživateli (např. povolání, projekty), témata, styl psaní
- chování: regenerace odpovědi, přeformulování dotazu, opravy („zkrať to“), zkopírování odpovědi, přerušení generování, opuštění konverzace

**Kontext**
- jazyk, země odvozená z IP, čas, zařízení atd.

## 2. Zpracování a uchování
1. **Extrakce:** po skončení konverzace (např. hodinu od poslední zprávy) jde událost do fronty a na pozadí ji zpracuje malý levný LLM. Výstupem jsou fakta, preference a krátké shrnutí konverzace. Extrakce běží jednou za konverzaci, ne u každé zprávy, takže náklady zůstanou únosné i při milionech konverzací denně. Výslovné pokyny („zapamatuj si…“) model ukládá hned během konverzace přes nástroj `save_memory`; i tyto záznamy pak projdou sloučením (bez duplicit) a tříděním do profilu nebo vektorové DB.
2. **Sloučení s existující pamětí:** pro každý údaj se rozhodne přidat / aktualizovat / smazat / nic. Pravidla priority: explicitní údaj má vždy přednost před implicitním, novější před starším. Co platí pro většinu konverzací, jde do profilu, situační detaily do vektorové DB.
3. **Uložení:**
   - **profil** (krátká fakta a preference, ~500 tokenů) -> key-value DB podle `user_id`
   - **shrnutí konverzací a detailnější fakta** -> embedding (vícejazyčný model, např. Qwen3-Embedding) -> vektorová DB (např. pgvector, Qdrant). Záznam = vektor + souhrn + metadata (`user_id`, čas, `conversation_id`)
   - **celé konverzace** -> historie chatu, neembedují se, slouží jako zdroj pro extrakci a jsou dostupné podle `user_id` + `conversation_id`

**Typy uživatelů:** uživatele periodicky shlukuji podle profilu a chování (např. „IT vývojář, chce odpovědi stručně“, „student, rád si nechává věci dlouze vysvětlovat“). Typ využívám jako:
- výchozí nastavení pro nové uživatele a náhradu za údaje profilu s nízkou jistotou (profil má vždy přednost),
- kontext pro testování nejistých údajů, kdy výsledky sčítám za celý typ, takže se rychleji naučí, co funguje,
- vodítko pro vedení konverzace (studentovi nabídnout procvičení, vývojáři rovnou kód) a pro výběr modelu (jednodušší dotazy -> menší, levnější model),
- dimenzi pro vyhodnocení: výsledky A/B testu rozdělím podle typů, protože celkové zlepšení může skrýt typy, kterým personalizace škodí; pro ty ji lze vypnout nebo upravit.
## 3. Využití při generování odpovědí
- **Vždy v system promptu:** profil + krátká shrnutí 3-5 posledních konverzací (podobně jako ChatGPT podle neoficiálních analýz [2]), pevný rozpočet ~1-2k tokenů.
- **Na vyžádání (RAG jako nástroj agenta):** `search_memory(query)`. Model ho volá, když usoudí, že potřebuje starší kontext, nejen na výslovný dotaz uživatele. Sám napíše krátký vyhledávací dotaz, ten se embeduje a ve vektorové DB se najde top-k záznamů (filtr na `user_id`, práh podobnosti). Do promptu jde text nalezených záznamů s datem.
- **Priorita:** pokyn v aktuální konverzaci > explicitní preference > implicitní preference > výchozí nastavení typu uživatele.

## 4. Vyhodnocení

**Offline (před nasazením)**
- testovací sada konverzací s pamětí; ke každému dotazu odpověď s personalizací i bez ní
- LLM jako soudce (párové porovnání): která odpověď lépe odpovídá preferencím uživatele, aniž by trpěla správnost. Shodu soudce s lidmi ověřím na vzorku lidských hodnocení, a pokud je shoda nízká, upravím jeho kritéria, aby se s lidmi shodoval víc.

**Testování nejistých údajů v profilu**
Kde má profil nízkou jistotu, systém občas vyzkouší jinou hodnotu a sleduje reakci. Odměna = palec nahoru, absence oprav, pokračování konverzace. Explorace jen na malém podílu odpovědí (např. 5 %) a nikdy proti explicitní preferenci. Vhodné dimenze:
- délka odpovědi: kratší vs. delší (jasný signál: žádost o zkrácení nebo o víc detailů, přerušení generování)
- formát: odrážky vs. souvislý text, s tabulkou nebo bez (uživatel pokračuje, nebo žádá přeformátování)
- úroveň odbornosti: jednodušší vs. technické vysvětlení

**Online A/B test (rozhodující)**
Uživatele (ne konverzace) náhodně rozdělím na kontrolní skupinu bez personalizace a skupinu s personalizací.

| Metrika | Proč |
|---|---|
| počet oprav stylu na konverzaci („zkrať“, „jednodušeji“, „píšeš divně“) | nejpřímější signál, že bot netrefil preferenci |
| podíl palců nahoru/dolů a regenerací | spokojenost s odpovědí |
| úspěšné dokončení konverzace (bez opakování dotazu) | uživatel dostal, co chtěl |
| 7/30denní retence, frekvence návratů | dlouhodobá hodnota |
| podíl uživatelů, kteří personalizaci vypnou | kontrolní metrika: nepříjemná nebo „creepy“ personalizace |
| latence, náklady na konverzaci | kontrolní metriky provozu |

Test běží dost dlouho, aby odezněl efekt novosti; výsledky dělím na nové a vracející se uživatele. Vrstvy zavádím po fázích (profil + shrnutí -> + RAG) a každou nechám, jen když prokazatelně pomáhá. Malá trvalá kontrolní skupina bez personalizace ukazuje efekt v čase.

## Reference
1. Zhang et al.: *Personalization of Large Language Models: A Survey*, TMLR. https://arxiv.org/abs/2411.00027
2. Gupta: *I Reverse Engineered ChatGPT's Memory System* (neoficiální analýza). https://manthanguptaa.in/posts/chatgpt_memory/