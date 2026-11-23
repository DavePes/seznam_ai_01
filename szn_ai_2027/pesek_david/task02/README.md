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

nastavení: např hlas chatbota, styl odpovědi, Custom instruction
implicitní 
palec nahoru/dolů na konkrétní odpověď chatbota, výběr mezi návrhy dvou odpovědí
 
Kontext:
např IP adresa, čas poslání zprávy, jazyk
