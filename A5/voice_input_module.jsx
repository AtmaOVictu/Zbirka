import { useState, useEffect } from "react";

export default function VoiceInputModule() {
  const [transcript, setTranscript] = useState("");
  const [listening, setListening] = useState(false);
  let recognition;

  useEffect(() => {
    if (typeof window !== "undefined" && "webkitSpeechRecognition" in window) {
      recognition = new webkitSpeechRecognition();
      recognition.lang = "sl-SI";
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onresult = (event) => {
        let interim = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            setTranscript((prev) => prev + event.results[i][0].transcript);
          } else {
            interim += event.results[i][0].transcript;
          }
        }
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error", event);
      };
    }
  }, []);

  const toggleListening = () => {
    if (!listening) {
      recognition.start();
      setListening(true);
    } else {
      recognition.stop();
      setListening(false);
    }
  };

  return (
    <div className="p-4 text-center">
      <button
        onClick={toggleListening}
        className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
      >
        {listening ? "🎙 Poslušam..." : "▶️ Aktiviraj govor"}
      </button>
      <div className="mt-4 text-sm bg-gray-100 p-2 rounded">
        {transcript || "🜂 Čakam na zvočni vnos..."}
      </div>
    </div>
  );
}
