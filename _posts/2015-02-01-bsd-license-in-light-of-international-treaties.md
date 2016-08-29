---
layout: post
title: A look at BSD in light of international treaties
category : copyright
tagline: "Digital Nomad"
tags : [bsd, international treaties]
---
{% include JB/setup %}

### BSD license in China

Last week, Ben Cotton [blogged](http://blog.funnelfiasco.com/wp-trackback.php?p=1638) about the initiative to rewrite BSD 3-clause license using only words from Oxford 3000 dictionary. The rewrite was prompted, as you can see in the linked blog, by a problem brought to light on [OSI's license-discuss](http://projects.opensource.org/pipermail/license-discuss/2015-January/001626.html) list about a Chinese developer using BSD license. It seems, from the facts we can glean so far, that the developer failed to enforce the simple conditions of the license in court, because the judge didn't understand English and threw out his complaint.

Without more information, we don't know what happened, and without information on specificity of Chinese copyright law, we can't quite rewrite the license even in English. I'm thinking we can do something else in the meantime, though.

I checked the membership of the main international treaties which lay out the minimum requirements for copyright protection, and found that China is a member of Berne Convention, WIPO and TRIPS. These treaties contain basics of copyright laws we know and assume true, regardless whether we work within a particular implementation in a country. There is more of a reason to assume the treaty provisions will be reflected in member states' legislation: some of these treaties contain not only recitals of exclusive rights and limitations, some are also trade agreements, thus contain sanctions against a member country that doesn't assure a certain expected implementation. I'd conclude it's reasonable to expect that if a provision is clearly required in these treaties, in more than one to be sure, then there is a corresponding implementation in the legal system of each signatory country.

If the above is too much for a ground of inquiry, then I can limit the statement to hoping that if we show how a license is based on the provisions of international copyright laws, it will be easier for a lawyer or judge in any country to recognize the corresponding elements of their local laws, and make an informed judgement on whether and how the license applies.

### Elements in Berne Convention

[Berne Convention](http://www.wipo.int/treaties/en/text.jsp?file_id=283698) text, article 2, states that "literary and artistic works"

> shall enjoy protection in all countries of the Union. This protection shall operate for the benefit of the author and his successors in title.

Sections (1), (3), (5) and (7) list the kinds of works that receive this protection, (1) enumerates what is understood by literary and artistic works, and the other sections specify additions to these works, such as adaptations, collections, and possibly (subject to national laws) applied industrial art and models.

Article 9 specified the exclusive right of reproduction:

> Authors of literary and artistic works protected by this Convention shall have the exclusive right of authorizing the reproduction of these works, in any manner or form.

There are criteria for authors whose works are protected, in the formerly mentioned art. 3:

> (a) authors who are nationals of one of the countries of the Union, for their works, whether published or not;
> (b) authors who are not nationals of one of the countries of the Union, for their works first published in one of those countries, or simultaneously in a country outside the Union and in a country of the Union.

Art. 3 also defines another detail: what means published works:

> works published with the consent of their authors, whatever may be the means of manufacture of the copies.

It's important because in the text of the Berne Convention there's little to no clear specification of an exclusive right of "distribution". Instead, reproduction of the works is an exclusive right that the treaty reserves for authors. Digital distribution implies reproduction (when you have a copy and distribute by such means that each of two or more recipients gets their own copy), and therefore distribution requires authorization from the author for those reproductions. Nevertheless, the definition of published works reinforces that: works published with consent of their authors.

Overall, the Berne Convention tries to assure that each country gives to foreign authors at least the protection that it gives to its nationals, and at a minimum the exclusive rights to do or authorize the actions listed in its articles: in particular reproduction.

There are other exclusive rights of less direct interest for software (though arguably of interest for documentation). There are also exceptions and limitations I won't get into, because every free and open source license respects them.

### Elements in WIPO Copyright Treaty

[WIPO Copyright Treaty](http://www.wipo.int/treaties/en/text.jsp?file_id=295166) explicitly defines the scope of copyright protection, exclusive rights, application to computer programs, technological measures and others. WIPO is an document which from the start (art. 1) explicitly incorporates the Berne Convention:

> Contracting Parties shall comply with Articles 1 to 21 and the Appendix of the Berne Convention.

A footnote on how to understand this incorporation refers to the reproduction right I mentioned above:

> The reproduction right, as set out in Article 9 of the Berne Convention, and the exceptions permitted thereunder, fully apply in the digital environment, in particular to the use of works in digital form. It is understood that the storage of a protected work in digital form in an electronic medium constitutes a reproduction within the meaning of Article 9 of the Berne Convention.

But WIPO doesn't limit to that. Its article 6 explicitly includes "right of distribution":

> Authors of literary and artistic works shall enjoy the exclusive right of authorizing the making available to the public of the original and copies of their works through sale or other transfer of ownership.

WIPO explicitly includes computer programs within the scope of "literary works":

> Computer programs are protected as literary works within the meaning of Article 2 of the Berne Convention. Such protection applies to computer programs, whatever may be the mode or form of their expression.

All signatories are bound to the treaty, according art. 18:

> Subject to any specific provisions to the contrary in this Treaty, each Contracting Party shall enjoy all of the rights and assume all of the obligations under this Treaty.

How about enforcement? Article 14 recites:

> Provisions on Enforcement of Rights

> (1) Contracting Parties undertake to adopt, in accordance with their legal systems, the measures necessary to ensure the application of this Treaty.
> (2) Contracting Parties shall ensure that enforcement procedures are available under their law so as to permit effective action against any act of infringement of rights covered by this Treaty, including expeditious remedies to prevent infringements and remedies which constitute a deterrent to further infringements. 

### Preliminary conclusions

Berne and WIPO Copyright Treaty, taken together, establish a base copyright framework upon which national legal systems are supposed to rest. On the other hand, this copyright framework they establish thus far is sufficient, it seems to me, to interpret free and open source licenses.

That doesn't mean there aren't surprises lurking in national implementations or court interpretations; there can well be. However, it seems worth the effort to interpret free and open source licenses in light of these generic provisions, relying less on a particular legal system.

The interpretation is strikingly simple: as a copyright license, a free and open source license grants authorization to do the acts reserved for the author(s), to any person getting a copy of the software, but only as long as they respect its conditions.

I'll look at BSD 3-clause license and Ben's Permissive 3000 in part 2.
