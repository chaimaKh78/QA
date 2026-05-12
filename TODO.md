# TODO - Flake8 cleanup

- [ ] accounts/admin.py: remove unused `UserAdmin` import
- [ ] accounts/apps.py: ignore/mark side-effect `import accounts.signals` to silence F401
- [ ] accounts/views.py: remove unused imports (TemplateView, UpdateView, reverse, User)
- [ ] bookings/models.py: remove unused `timezone` import
- [ ] bookings/views.py: remove unused imports (TemplateView, reverse, Passenger, Payment, PaymentForm)
- [ ] destinations/views.py: remove unused imports (render/get_object_or_404, timezone, DestinationReview, Flight/Airport) if unused
- [ ] promotions/views.py: remove unused imports (render, messages, JsonResponse, View, timezone) if unused
- [ ] nouvelair/settings.py: remove unused `os` and `timedelta`; move `reverse_lazy` import to top
- [ ] nouvelair/urls.py: ensure file ends with newline (W292)
- [ ] playwright.config.py: fix E302 spacing (2 blank lines before top-level def)
- [ ] conftest.py (repo root): move imports to top, remove trailing whitespace, ensure newline at EOF
- [ ] Re-run flake8 with the provided command and fix any remaining issues

