"use client"
import Link from "next/link";
import { Accordion, AccordionTab } from "primereact/accordion";
import DiscordLink from "../discordLink";
import { useState } from "react";

export default function FaqPage() {
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <div className="page-faq">
      <h1>FAQ</h1>
      <p>
        Welcome to the FAQ page! Hopefully this page will answer any pressing
        questions you may have about how to use TEA Tools. If you don't find an
        answer, reach out to us over on our <DiscordLink showText={true} />!
      </p>

      <p>Found what you need? Head back to the <Link href="/search">search page</Link> and start exploring!</p>

      <Accordion activeIndex={activeIndex}>
        <AccordionTab header="So how does this work?">
          <div>
            <p>
              Pretty simple really! Head over to the{" "}
              <Link href="/search">search page</Link> and enter in some text.
              Once you search, the page should display matching results from the
              game data text files.
            </p>
            <p>Some things of note:</p>
            <ul>
              <li>The search looks inside the title and text.</li>
              <li>
                The search matches whole words. For example, if you search for
                `ours` it will not match `yours` or `hours`.
              </li>
              <li>The results contain items that match <b>all</b> words entered in the text box <em>in any order</em>.</li>
              <li>You can quote your entire search string to make it match only that phrase (the words in specific order).</li>
              <li>
                The filter selections work to narrow down results. Note that the
                `Expansions` filter will <b>only</b> work with the types for
                `Quest` and `Cutscene`
              </li>
            </ul>
          </div>
        </AccordionTab>
        <AccordionTab header="I don't see something in the results. Where is it?">
          <div>
            Not every possible bit of text from the game is stored in our search
            engine. Unfortunately there are some limitations to what data we can
            extract. If you feel there is something missing that you should be
            able to find, come over to our <DiscordLink showText={true} /> and let us know!
          </div>
        </AccordionTab>
        <AccordionTab header="What if I have more questions?">
          <div>
            The easiest way is to join our <DiscordLink showText={true} /> and reach out!
          </div>
        </AccordionTab>
      </Accordion>
    </div>
  );
}
