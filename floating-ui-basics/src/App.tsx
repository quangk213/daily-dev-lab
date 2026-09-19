import { useEffect, useRef } from "react";
import "./App.css";
import { computePosition } from "@floating-ui/react";

function App() {
  const buttonRef = useRef(null);
  const tooltipRef = useRef(null);

  useEffect(() => {
    if (buttonRef.current && tooltipRef.current) {
      computePosition(buttonRef.current, tooltipRef.current).then(
        ({ x, y }) => {
          if (tooltipRef.current) {
            Object.assign(tooltipRef.current?.style, {
              left: `${x}px`,
              top: `${y}px`,
            });
          }
        },
      );
    }
  }, []);

  return (
    <div className="p-1">
      <button ref={buttonRef} className="bg-blue-300">
        My button
      </button>
      <div
        ref={tooltipRef}
        className="w-max absolute top-0 left-0 bg-[#222] text-white p-1 rounded-sm text-sm"
      >
        My tooltip
      </div>
    </div>
  );
}

export default App;
