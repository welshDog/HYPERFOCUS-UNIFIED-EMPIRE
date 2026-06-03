# Contributing to HYPERFOCUS UNIFIED EMPIRE

First off, thanks for thinking about contributing! This project is built BY neurodivergent minds, FOR everyone. Your perspective matters. 🧠✨

## Code of Conduct

Please review `CODE_OF_CONDUCT.md` before participating. We're committed to providing a welcoming, harassment-free experience for everyone.

## Ways to Contribute

### 🐛 Report Bugs
Found a bug? Great catch!

1. Check if it's already reported in [Issues](https://github.com/welshDog/HYPERFOCUS-UNIFIED-EMPIRE/issues)
2. Use the **Bug Report** template when creating a new issue
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Your environment details

### ✨ Suggest Features
Have an idea? We love hearing them!

1. Check [existing discussions](https://github.com/welshDog/HYPERFOCUS-UNIFIED-EMPIRE/discussions)
2. Start a **Feature Discussion** with:
   - What problem does this solve?
   - How does it support the neurodivergent community?
   - Example use case

### 📝 Improve Documentation
Typos? Confusing sections? Missing guides?

- Documentation PRs are always welcome
- Fix typos, clarify instructions, add examples
- No approval needed for small doc fixes

### 💻 Submit Code

#### Setup
```bash
git clone https://github.com/welshDog/HYPERFOCUS-UNIFIED-EMPIRE
cd HYPERFOCUS-UNIFIED-EMPIRE
pip install -r requirements.txt
```

#### Before You Code
1. Check open issues/PRs to avoid duplicate work
2. For larger changes, open an issue first to discuss approach
3. Follow the existing code style

#### Making Changes
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description

# Make your changes...
python -m pytest tests/        # Run tests
python -m pylint src/          # Check code style

git add .
git commit -m "✨ Brief description of change"
git push origin feature/your-feature-name
```

#### PR Guidelines
- Keep PRs focused (one feature/fix per PR)
- Link to related issues: `Closes #123`
- Include screenshots for UI changes
- Update tests if you changed functionality
- Update documentation if you changed behavior

## Development Guidelines

### Code Style
- Use **Black** for formatting
- Use **Pylint** for linting
- Follow existing patterns in the codebase

### Commits
- Use clear, descriptive commit messages
- Start with emoji: `✨` (feature), `🐛` (fix), `📝` (docs), `🔧` (config)
- Example: `✨ Connect HyperCode-V2.4 with BROski ecosystem`

### Testing
- Write tests for new features
- Ensure all tests pass: `python -m pytest`
- Aim for >80% coverage on new code

### Ecosystem Integration
- Document how your change connects ecosystem components
- Include integration tests
- Test with multiple sub-projects
- Follow the unified architecture patterns

## Questions or Need Help?

- **Discord:** [Join the BROski Community](#)
- **Discussions:** Start a [GitHub Discussion](https://github.com/welshDog/HYPERFOCUS-UNIFIED-EMPIRE/discussions)
- **Email:** See `SECURITY.md` for contact info

## Recognition

Contributors are recognized in:
- 📌 README.md (Contributors section)
- 🏆 Releases (when your code ships)
- 💰 BROski$ tokens (if applicable)

## License

By contributing, you agree your work will be licensed under `AGPL-3.0`. See `LICENSE` for details.

---

**Thank you for building the neurodivergent-first AI empire! 🚀**
