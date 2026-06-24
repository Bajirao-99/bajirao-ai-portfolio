import {
  useEffect,
  useRef,
} from "react";

const VISITED_KEY =
  "bajirao-portfolio-visited";

const SESSION_SPOKEN_KEY =
  "bajirao-portfolio-welcome-spoken-session";

function getWelcomeMessage(): string {
  const hasVisitedBefore =
    localStorage.getItem(VISITED_KEY) === "true";

  return hasVisitedBefore
    ? "Welcome back to Bajirao's portfolio."
    : "Welcome to Bajirao's portfolio.";
}

export default function WelcomeVoice() {
  const spokenRef = useRef(false);

  useEffect(() => {
    function speakWelcome(): void {
      if (spokenRef.current) {
        return;
      }

      if (
        sessionStorage.getItem(
          SESSION_SPOKEN_KEY,
        ) === "true"
      ) {
        return;
      }

      if (!("speechSynthesis" in window)) {
        return;
      }

      const message = getWelcomeMessage();

      const utterance =
        new SpeechSynthesisUtterance(message);

      utterance.lang = "en-IN";
      utterance.rate = 0.92;
      utterance.pitch = 1;
      utterance.volume = 0.8;

      utterance.onstart = () => {
        spokenRef.current = true;

        sessionStorage.setItem(
          SESSION_SPOKEN_KEY,
          "true",
        );

        localStorage.setItem(
          VISITED_KEY,
          "true",
        );
      };

      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    }

    const timer = window.setTimeout(
      speakWelcome,
      900,
    );

    const handleFirstInteraction = () => {
      speakWelcome();
    };

    window.addEventListener(
      "click",
      handleFirstInteraction,
      { once: true },
    );

    window.addEventListener(
      "pointerdown",
      handleFirstInteraction,
      { once: true },
    );

    window.addEventListener(
      "keydown",
      handleFirstInteraction,
      { once: true },
    );

    window.addEventListener(
      "scroll",
      handleFirstInteraction,
      { once: true, passive: true },
    );

    return () => {
      window.clearTimeout(timer);

      window.removeEventListener(
        "click",
        handleFirstInteraction,
      );

      window.removeEventListener(
        "pointerdown",
        handleFirstInteraction,
      );

      window.removeEventListener(
        "keydown",
        handleFirstInteraction,
      );

      window.removeEventListener(
        "scroll",
        handleFirstInteraction,
      );
    };
  }, []);

  return null;
}