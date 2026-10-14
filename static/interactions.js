const feedbackDialog = document.querySelector("#feedback-dialog");
const mailboxDialog = document.querySelector("#mailbox-dialog");

document.querySelectorAll("[data-feedback-open]").forEach((button) => {
  button.addEventListener("click", () => feedbackDialog?.showModal());
});

document.querySelectorAll("[data-feedback-close]").forEach((button) => {
  button.addEventListener("click", () => feedbackDialog?.close());
});

document.querySelectorAll("[data-category]").forEach((button) => {
  button.addEventListener("click", () => {
    const category = button.dataset.category;
    const formStep = feedbackDialog.querySelector('[data-feedback-step="form"]');
    feedbackDialog.querySelector('[data-feedback-step="choose"]').hidden = true;
    formStep.hidden = false;
    formStep.querySelector(".selected-category-title").textContent = `${category} bırakın`;
    formStep.querySelector('input[name="category"]').value = category;
    formStep.querySelector('input[name="title"]').focus();
  });
});

document.querySelector("[data-feedback-back]")?.addEventListener("click", () => {
  feedbackDialog.querySelector('[data-feedback-step="form"]').hidden = true;
  feedbackDialog.querySelector('[data-feedback-step="choose"]').hidden = false;
});

feedbackDialog?.addEventListener("click", (event) => {
  if (event.target === feedbackDialog) feedbackDialog.close();
});

feedbackDialog?.addEventListener("close", () => {
  feedbackDialog.querySelector('[data-feedback-step="form"]').hidden = true;
  feedbackDialog.querySelector('[data-feedback-step="choose"]').hidden = false;
  feedbackDialog.querySelector("form").reset();
});

document.querySelector("[data-mailbox-open]")?.addEventListener("click", () => mailboxDialog?.showModal());
document.querySelector("[data-mailbox-close]")?.addEventListener("click", () => mailboxDialog?.close());
mailboxDialog?.addEventListener("click", (event) => {
  if (event.target === mailboxDialog) mailboxDialog.close();
});