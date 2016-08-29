---
layout: post
title: EFF is suing over unconstitutionality of DMCA 1201
category : copyright
tagline: "Digital Nomad"
tags : [EFF-v-US, DMCA, freedom of speech]
---
{% include JB/setup %}

Cory Doctorow blogged about the news that EFF filed a suit against US government for the unconstitutionality of DMCA paragraph 1201.

Finally! I was waiting for this to happen. Cory Doctorow mentioned before in his talks, in the late years, that he went back to work with the EFF on this law. In order for a court to strike it down though, they need a case. A good case, that is, and security research can provide a lot of examples.

Now, EFF is assisting not one, but two plaintiffs. According to Cory, Andrew "bunnie" Huang, with a PhD from MIT, and Matthew Green, an assistant professor from Johns Hopkins who has a grant to study medical software devices, are the plaintiffs. They are directly affected by DMCA 1201 in their work. The section incriminates "circumvention" of "access controls" to a copyrighted work, in other words, most usually known as DRM.

To step back in time a little, there's this detail here: in Universal v Corley, the movie studio won their case under DMCA 1201 against the hacker magazine for publishing the code that can be used to descramble a DVD. I remember the surprise of those involved the case, because you see, it was "the same thing" that happened before, when free speech argument had won the day, but now they lost. Why did they lose that case? Reading the decision, I remember thinking that the judge basically made up his mind, and he's just adding arguments that could look entirely different if you didn't come to the case with some impression of something wrong. I think the problem was human nature interfering with reasoning: the magazine was suspected to not publish only "white hats" work. It "looked suspicious", I'd say. It was a wrong decision, and the people involved were not crackers. But I think things surrounding the case have mattered back then.

Today we see two researchers with years of experience, worldwide known university names, an impeccable reputation, and even, in Matthew's case, we see a grant to perform the work he's supposed to perform: research medical devices. Those devices are no longer our good ole' stethoscope, but like usual nowadays, they contain software. Software is a copyrighted work, and any access controls added to that work may fall under DMCA, so their "circumvention" will run afoul of DMCA 1201. It does not matter if you didn't intend anything illegal for other reasons, you still fall under this section.

Here are a few relevant passages of DMCA 1201 that apply to their work:

> (a)Violations Regarding Circumvention of Technological Measures.—

> (1)

> (A) No person shall circumvent a technological measure that effectively controls access to a work protected under this title. [...] 

> (2) No person shall manufacture, import, offer to the public, provide, or otherwise traffic in any technology, product, service, device, component, or part thereof, that—
> (A) is primarily designed or produced for the purpose of circumventing a technological measure that effectively controls access to a work protected under this title;
> (B) has only limited commercially significant purpose or use other than to circumvent a technological measure that effectively controls access to a work protected under this title; or
> (C) is marketed by that person or another acting in concert with that person with that person’s knowledge for use in circumventing a technological measure that effectively controls access to a work protected under this title.

Interestingly,

> (e)Law Enforcement, Intelligence, and Other Government Activities.—

> This section does not prohibit any lawfully authorized investigative, protective, information security, or intelligence activity of an officer, agent, or employee of the United States, a State, or a political subdivision of a State, or a person acting pursuant to a contract with the United States, a State, or a political subdivision of a State. For purposes of this subsection, the term “information security” means activities carried out in order to identify and address the vulnerabilities of a government computer, computer system, or computer network.

The above paragraph seems to say that the lawmakers felt there is something wrong with the prohibition, which is why it shouldn't be used against security researchers employed by the United States government. Well, that leaves the other security researchers out in the cold.

There are also a few exemptions for particular "encryption" cases, but they don't cover - far from it - the whole area put to risk by DMCA 1201. [Here](https://www.law.cornell.edu/uscode/text/17/1201) is the whole text of DMCA section 1201.

There's another interesting detail in the history of court cases to challenge this section, and Cory saves me from looking it up, by mentioning it in his [The Guardian article](https://www.theguardian.com/technology/2016/jul/21/digital-millennium-copyright-act-eff-supreme-court) on this:

> When Ed Felten - a prominent computer scientist, then at Princeton University, now deputy CTO of the White House – and a group of peers published a paper on defects in DRM for music called Secure Digital Music Initiative, the record companies threatened to sue him and the technical conference where the paper was to be delivered. The Electronic Frontier Foundation stepped forward to defend Felten, and the labels beat all speed records withdrawing their threats because they understood that judges would be reluctant to give record executives a veto over the kinds of technical presentations that computer scientists could give.

This gives us a little insight into how court cases work. You see, the labels knew this was going to be a bad case (for them, and probably good for everyone else) when they looked closer, so they stepped back from that. Leaving us with the former bad case (for everyone else than them), and with the unsettled issue of DRM and free speech. If code is a way to express things (and it is), then this section of DMCA, which criminalizes free expression, in itself, is indeed unconstitutional in US.

