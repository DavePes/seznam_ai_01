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
## Explicitní data (uživatel je řekne nebo nastaví sám)

nastavení: jazyk, tón, délka odpovědí, úroveň odbornosti
přímé pokyny: „zapamatuj si…“, „odpovídej stručněji“
zpětná vazba: palec nahoru/dolů, výběr mezi dvěma odpověďmi (pairwise)