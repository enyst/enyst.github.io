---
layout: post
title: A look at BSD in light of international treaties, part 2
category : copyright
tagline: "Digital Nomad"
tags : [bsd, international treaties]
---
{% include JB/setup %}

In the first part, I read several articles of Berne Convention and WIPO Copyright Treaty, with the purpose to detect the basics of copyright protection that their member countries agree to implement. My intention is to see how to interpret free and open source licenses, old and new, informed by this quick analysis.

### BSD 3-clause license

Let us read BSD 3-clause license, informed by Berne and WCT.

The author or copyright holder of this computer program (WCT art. 4) or documentation (Berne art. 2) has the exclusive rights to:

> * reproduce and authorize reproduction of the work (Berne art. 9, WCT agreed statement),
> * authorize the distribution (making available to the public) of the original and copies of their work (WCT art. 6),
> * authorize translations (Berne art. 8) and other derivative works (Berne art. 12).

Instead of reserving all these rights, the author grants authorization to others, under conditions. The license says:

> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
> 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

The author _authorizes_ (or gives permission for) redistribution and use in source and binary forms, with or without modification. In Berne/WCT words, the author is the only one who can authorize the actions enumerated above. By this license, the author authorizes: distribution of copies of the work (redistribution without modification), both source and binary, and distribution of derivative works, translations or other adaptations (redistribution with modification).

Authorizes _who_? Who comes in possession of this software or documentation. The text itself says that all copies (redistributions of source code and redistributions in binary form) must retain or reproduce "the above copyright notice, this list of conditions and the following disclaimer". Therefore, the next person in possession of the software or documentation will obtain possession with this text attached.

In exchange for what does the author authorize these actions? In exchange for doing what the conditions 1, 2, and 3 say:
* Distribution of a copy or derivative work in source code is authorized provided that it retains the copyright notice, the list of terms and conditions, and the disclaimer.
* Distribution of binary forms of this software is authorized provided that it reproduces the copyright notice, the conditions and disclaimer in the documentation and/or other materials provided with the binary.
* The distributor is not authorized to use the name of the author(s) to claim that they endorse or to promote products derived from the software (without another, different, written permission).

If someone redistributes without respecting these three conditions, they are not authorized. The distribution that doesn't abide by the conditions is infringing copyright of the author, because authorization was given only under these conditions.

### Permissive 3000 license

Let us turn for a minute to [Permissive 3000](https://github.com/funnelfiasco/permissive3000/blob/master/license.txt) license. This is an experimental text, written with the purpose to express the same thing as BSD 3-clause, using only words in [Oxford 3000](http://www.oxfordlearnersdictionaries.com/us/wordlist/english/oxford3000/) list. In its current form, it looks like this:

> Distribution and use in source and object forms, with or without changes, are
permitted provided that the following conditions are met:

> 1. Distribution of source code must retain the above copyright notice, this list of conditions and the following refusal of responsibility.
> 2. Distribution in object form must reproduce the above copyright notice, this list of conditions and the following refusal of responsibility in ddocuments and/or other materials provided with the distribution.
> 3. The name of the author or authors may not be used to recommend or advertise works derived from this software without specific prior written permission.

Instead of redistribution, it says distribution. That's arguably more appropriate for our purposes because it's the same term used in WCT: the right of distribution is an exclusive right of the author. With or without changes stands for with or without modifications. That seems acceptable, in English the two are synonyms, and the combined meaning here is of course copies of original works and derivative works.
"Refusal of responsibility" sounds odd in English, particularly when it's supposed to stand for disclaimer, and one can argue it's problematic because disclaimer and disclaimer of liability are terms of art.
The 3rd clause uses recommend and advertise for endorse and promote, which seems acceptable. This clause is a little odd in a copyright license, but it doesn't really say anything more than what is probably true anyway: that one is shielded from having their name used to claim things they don't do, such as endorse _another_ software they have no idea about, and this license does not authorize any subsequent author or distributor to do that.

Apart from the main body of the text, BSD and Permissive 3000 contain the no-warranty clause. That intends to disclaim any warranty, which is easily understood because the author who licenses their work with BSD is offering the work for free, in any stage of development. It would be entirely unreasonable for someone to expect any warranty, absent, on the contrary, an express written intention to provide warranty for a particular version and explicitly offer warranty.

We could also look at TRIPS. I'm not doing that here; already, within the framework sketched by Berne and WIPO Copyright Treaty, there are enough elements to ground a copyright license like BSD on, because it's that simple. It merely says that authorization to do those things reserved for the author of a computer software or documentation is given, to those who do "retain" or "reproduce" the text.
