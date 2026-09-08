const focus = document.querySelector("#focus");
const status = document.querySelector("#status");
const selectButton = document.querySelector("#select");

// In a toolbar popup, this is the window containing the popup.
const currentWindowPromise = chrome.windows.getCurrent();

function show(message, isError = false) {
  status.textContent = message;
  status.style.color = isError ? "#b42318" : "#175b39";
}

async function init() {
  const [currentWindow, session, saved] = await Promise.all([
    currentWindowPromise,
    chrome.storage.session.get("targetWindowId"),
    chrome.storage.local.get(["focusTarget", "lastError"]),
  ]);

  focus.checked = saved.focusTarget ?? true;

  if (saved.lastError) {
    show(saved.lastError, true);
  } else if (session.targetWindowId === currentWindow.id) {
    show("This window is the target.");
  } else if (session.targetWindowId != null) {
    show("Another window is selected as the target.");
  } else {
    show("No target window selected.");
  }
}

selectButton.addEventListener("click", async () => {
  try {
    const currentWindow = await currentWindowPromise;

    if (currentWindow.type !== "normal" || currentWindow.incognito) {
      throw new Error("Select a normal Chrome window.");
    }

    await chrome.storage.session.set({
      targetWindowId: currentWindow.id,
    });

    await chrome.storage.local.set({
      focusTarget: focus.checked,
    });

    await chrome.storage.local.remove("lastError");
    await chrome.action.setBadgeText({ text: "" });

    show("This window will now receive your links.");
  } catch (error) {
    show(error.message, true);
  }
});

focus.addEventListener("change", async () => {
  try {
    await chrome.storage.local.set({
      focusTarget: focus.checked,
    });
  } catch (error) {
    show(error.message, true);
  }
});

init().catch((error) => show(error.message, true));
