# Structure

One folder per law at the top level, named after its short title (`employment/`, `companies/`); a second law with the same name gets its year (`finance-2016/`). The Constitution is `constitution/`.

- **By section** (most Acts): one file per section, `sec-NNN.md` (`sec-071.md` is section 71), plus `sch-NN.md` for schedules and `README.md` listing the provisions.
- **Whole text** (the Acts listed below): one file, `text.md`, holding the Act as printed from its title to the printer's colophon, where the print's text layer is complete but could not be split into one file per section (side notes printed on the same line as the section number, two-column prints, Appropriation schedules). Their commits carry `Layout: whole text`. Each was checked to hold sections 1 to N in order, N being the last number of the printed Arrangement of Sections, and no repeated page; copies with missing pages are not here.

Each version is one commit dated noon (Africa/Freetown, GMT) on the day it took effect, with `In-force:` and `In-force-basis:` trailers; see README.md.

## Whole-text Acts (38)

| Folder | Act | Law | In force | Source |
| --- | --- | --- | --- | --- |
| `anti-corruption/` | The Anti-Corruption Act, 2000 | Act No. 1 of 2000 | 2000-02-03 | secondary copy |
| `anti-money-laundering/` | The Anti-Money Laundering Act, 2005 | Act No. 6 of 2005 | 2005-07-21 | official print |
| `anti-money-laundering-combating-financing-terrorism/` | The Anti Money Laundering and Combating of Financing of Terrorism Act, 2012 | Act No. 2 of 2012 | 2012-03-15 | official print |
| `appropriation/` | The Appropriation Act, 2005 | Act No. 4 of 2005 | 2005-06-09 | official print |
| `appropriation-2006/` | The Appropriation Act, 2006 | Act No. 8 of 2006 | 2006-06-22 | official print |
| `appropriation-2007/` | The Appropriation Act, 2007 | Act No. 1 of 2007 | 2007-04-05 | official print |
| `appropriation-2008/` | The Appropriation Act, 2008 | Act No. 3 of 2008 | 2008-05-22 | official print |
| `appropriation-2019/` | The Appropriation Act, 2019 | Act No. 1 of 2019 | 2019-01-11 | official print |
| `appropriation-2021/` | The Appropriation Act, 2021 | Act No. 2 of 2021 | 2021-01-28 | official print |
| `appropriation-2022/` | The Appropriation Act, 2022 | Act No. 2 of 2022 | 2022-01-13 | official print |
| `arms-ammunition/` | The Arms and Ammunition Act, 2012 | Act No. 9 of 2012 | 2012-08-30 | official print |
| `assented-her-majesty-s-name-this-5th-day-june-1963-h-j-l-boston-govern/` | The Assented to in Her Majesty’s name this 5th day of June, 1963. H. J. L. BOSTON, Governor-General. LS A 137 3, 20, and 28 of the Crown Lands Act, 1960 | Act No. 37 of 1961 | 1965-06-10 | secondary copy |
| `civil-aviation/` | The Civil Aviation Act, 2019 | Act No. 7 of 2019 | 2019-08-29 | official print |
| `entertainment-tax-amendment/` | The Entertainment Tax (Amendment) Act, 2004 | Act No. 12 of 2004 | 2004-04-01 | official print |
| `finance-2010/` | The Finance Act, 2010 | Act No. 2 of 2010 | 2010-01-01 | official print |
| `finance-2011/` | The Finance Act, 2011 | Act No. 12 of 2011 | 2011-11-10 | official print |
| `finance-2014/` | The Finance Act, 2015 | Act No. 15 of 2014 | 2014-12-30 | secondary copy |
| `finance-2017/` | The Finance Act, 2017 | Act No. 1 of 2017 | 2017-06-08 | official print |
| `goods-services-tax/` | The Goods and Services Tax Act, 2009 | Act No. 6 of 2009 | 2009-09-01 | official print |
| `guma-valley-water-company/` | The Guma Valley Water Company Act, 2017 | Act No. 6 of 2017 | 2017-08-17 | official print |
| `human-rights-commission-sierra-leone/` | The Human Rights Commission of Sierra Leone Act, 2004 | Act No. 9 of 2004 | 2004-08-26 | official print |
| `income-tax/` | The Income Tax Act, 2000 | Act No. 8 of 2000 | 2000-06-15 | secondary copy |
| `investment-promotion/` | The Investment Promotion Act, 2004 | Act No. 10 of 2004 | 2004-08-26 | official print |
| `legal-practitioners-amendment-2015/` | The Legal Practitioners (Amendment) Act, 2015 | Act No. 2 of 2015 | 2015-08-06 | official print |
| `merchant-shipping/` | The Merchant Shipping Act, 2003 | Act No. 3 of 2003 | 2003-07-10 | secondary copy |
| `mines-minerals/` | The Mines and Minerals Act, 2009 | Act No. 12 of 2009 | 2010-01-07 | official print |
| `national-communications-authority/` | The National Communications Authority Act, 2022 | Act No. 16 of 2022 | 2022-09-16 | official print |
| `national-electoral-commission/` | The National Electoral Commission Act, 2002 | Act No. 1 of 2002 | 2002-02-07 | secondary copy |
| `public-debt-management/` | The Public Debt Management Act, 2011 | Act No. 2 of 2011 | 2011-03-24 | official print |
| `public-order/` | The Public Order Act, 1965 | Act No. 46 of 1965 | 1965-12-31 | secondary copy |
| `residual-special-court-sierra-leone-agreement-ratification/` | The Residual Special Court for Sierra Leone Agreement (Ratification) Act, 2011 | Act No. 1 of 2012 | 2012-02-09 | official print |
| `road-maintenance-fund-administration/` | The Road Maintenance Fund Administration Act, 2010 | Act No. 3 of 2010 | 2010-04-15 | official print |
| `sierra-leone-peace-keeping-law-enforcement-academy/` | The Sierra Leone Peace Keeping and Law Enforcement Academy Act, 2017 | Act No. 7 of 2017 | 2017-08-31 | official print |
| `sierra-leone-produce-marketing-repeal/` | The Sierra Leone Produce Marketing Act (Repeal) Act, 2013 | Act No. 1 of 2013 | 2013-08-01 | official print |
| `state-salaries-pensions-gratuities-other-benefits-2001/` | The State Salaries, Pensions, Gratuities and Other Benefits Act, 2001 | Act No. 1 of 2001 | 2001-05-03 | secondary copy |
| `supplementary-appropiation/` | The Supplementary Appropiation Act, 2022 | Act No. 1 of 2022 | 2022-01-07 | official print |
| `supplementary-appropriation/` | The Supplementary Appropriation Act, 2014 | Act No. 12 of 2014 | 2014-12-30 | official print |
| `supplementary-appropriation-2018/` | The Supplementary Appropriation Act, 2018 | Act No. 13 of 2018 | 2018-07-19 | official print |
