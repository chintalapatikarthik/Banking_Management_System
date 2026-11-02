// Main application UI logic & interactions
document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Sidebar Toggle
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('appSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('show');
            if (overlay) overlay.classList.toggle('show');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }

    // 2. Real-time Header Clock
    const clockEl = document.getElementById('realtimeClock');
    if (clockEl) {
        const updateClock = () => {
            const now = new Date();
            clockEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        };
        updateClock();
        setInterval(updateClock, 1000);
    }

    // 3. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });

    // 4. Form balance preview helpers for financial ops
    const amountInput = document.getElementById('transAmount');
    const sourceAccSelect = document.getElementById('sourceAccountSelect');
    const balancePreview = document.getElementById('balancePreview');

    if (amountInput && sourceAccSelect && balancePreview) {
        const updatePreview = () => {
            const selectedOpt = sourceAccSelect.options[sourceAccSelect.selectedIndex];
            const currentBal = parseFloat(selectedOpt?.dataset?.balance || 0);
            const enteredAmt = parseFloat(amountInput.value || 0);
            const isWithdraw = document.getElementById('opType')?.value === 'withdraw';

            if (isNaN(enteredAmt) || enteredAmt <= 0) {
                balancePreview.innerHTML = `Current Balance: <strong>₹${currentBal.toLocaleString('en-IN', {minimumFractionDigits: 2})}</strong>`;
                return;
            }

            if (isWithdraw) {
                const rem = currentBal - enteredAmt;
                if (rem < 0) {
                    balancePreview.innerHTML = `<span class="text-danger fw-bold"><i class="bi bi-exclamation-triangle"></i> Insufficient Balance! Deficit: ₹${Math.abs(rem).toLocaleString('en-IN', {minimumFractionDigits: 2})}</span>`;
                } else {
                    balancePreview.innerHTML = `New Balance: <strong class="text-success">₹${rem.toLocaleString('en-IN', {minimumFractionDigits: 2})}</strong> (Deducting ₹${enteredAmt.toLocaleString('en-IN', {minimumFractionDigits: 2})})`;
                }
            } else {
                const newBal = currentBal + enteredAmt;
                balancePreview.innerHTML = `New Balance: <strong class="text-success">₹${newBal.toLocaleString('en-IN', {minimumFractionDigits: 2})}</strong> (Crediting ₹${enteredAmt.toLocaleString('en-IN', {minimumFractionDigits: 2})})`;
            }
        };

        amountInput.addEventListener('input', updatePreview);
        sourceAccSelect.addEventListener('change', updatePreview);
    }
});

// Copy text utility
function copyToClipboard(text, btnElement) {
    navigator.clipboard.writeText(text).then(() => {
        const originalHtml = btnElement.innerHTML;
        btnElement.innerHTML = '<i class="bi bi-check2"></i> Copied!';
        btnElement.classList.add('btn-success');
        btnElement.classList.remove('btn-outline-secondary');
        setTimeout(() => {
            btnElement.innerHTML = originalHtml;
            btnElement.classList.remove('btn-success');
            btnElement.classList.add('btn-outline-secondary');
        }, 2000);
    });
}
