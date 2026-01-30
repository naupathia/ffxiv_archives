import Link from "next/link";
import { FaDiscord } from "react-icons/fa"; // Example from react-icons/fa

const DiscordLink = ({ showText = false }) => {
  return (
    <Link
      href="https://discord.gg/eorzeanarchives"
      passHref
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Join our Discord server"
    >
      {showText ? "Discord" : <FaDiscord size="32" className="discord-icon" />}
    </Link>
  );
};

export default DiscordLink;
