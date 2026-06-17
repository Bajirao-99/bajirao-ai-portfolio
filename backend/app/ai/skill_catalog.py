import re
from collections.abc import Iterable


SKILL_ALIASES: dict[str, set[str]] = {
    "Python": {
        "python",
    },
    "C": {
        "c",
    },
    "C++": {
        "c++",
        "cpp",
    },
    "C#": {
        "c#",
        "c sharp",
    },
    "Java": {
        "java",
    },
    "JavaScript": {
        "javascript",
        "java script",
        "js",
    },
    "TypeScript": {
        "typescript",
        "type script",
        "ts",
    },
    "HTML": {
        "html",
        "html5",
    },
    "CSS": {
        "css",
        "css3",
    },
    "React": {
        "react",
        "react.js",
        "reactjs",
    },
    "Next.js": {
        "next.js",
        "nextjs",
        "next js",
    },
    "Node.js": {
        "node.js",
        "nodejs",
        "node js",
    },
    "Express.js": {
        "express",
        "express.js",
        "expressjs",
    },
    "Angular": {
        "angular",
        "angular.js",
        "angularjs",
    },
    "Vue.js": {
        "vue",
        "vue.js",
        "vuejs",
    },
    "Tailwind CSS": {
        "tailwind",
        "tailwind css",
        "tailwindcss",
    },
    "Bootstrap": {
        "bootstrap",
    },
    "FastAPI": {
        "fastapi",
        "fast api",
    },
    "Django": {
        "django",
    },
    "Flask": {
        "flask",
    },
    "Spring Boot": {
        "spring boot",
        "springboot",
    },
    "REST APIs": {
        "rest api",
        "rest apis",
        "restful api",
        "restful services",
    },
    "GraphQL": {
        "graphql",
        "graph ql",
    },
    "Microservices": {
        "microservices",
        "micro services",
        "microservice architecture",
    },
    "SQL": {
        "sql",
    },
    "PostgreSQL": {
        "postgresql",
        "postgres",
        "postgre sql",
    },
    "MySQL": {
        "mysql",
        "my sql",
    },
    "SQLite": {
        "sqlite",
    },
    "MongoDB": {
        "mongodb",
        "mongo db",
    },
    "Redis": {
        "redis",
    },
    "Oracle": {
        "oracle database",
        "oracle db",
    },
    "SQLAlchemy": {
        "sqlalchemy",
        "sql alchemy",
    },
    "Machine Learning": {
        "machine learning",
        "ml",
    },
    "Deep Learning": {
        "deep learning",
        "dl",
    },
    "Artificial Intelligence": {
        "artificial intelligence",
        "ai",
    },
    "Natural Language Processing": {
        "natural language processing",
        "nlp",
    },
    "Large Language Models": {
        "large language model",
        "large language models",
        "llm",
        "llms",
    },
    "RAG": {
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
    },
    "Generative AI": {
        "generative ai",
        "genai",
        "gen ai",
    },
    "Computer Vision": {
        "computer vision",
        "image processing",
    },
    "TensorFlow": {
        "tensorflow",
        "tensor flow",
    },
    "PyTorch": {
        "pytorch",
        "py torch",
    },
    "Keras": {
        "keras",
    },
    "scikit-learn": {
        "scikit-learn",
        "scikit learn",
        "sklearn",
    },
    "Pandas": {
        "pandas",
    },
    "NumPy": {
        "numpy",
        "num py",
    },
    "Hugging Face": {
        "hugging face",
        "huggingface",
        "transformers",
    },
    "LSTM": {
        "lstm",
        "long short-term memory",
        "long short term memory",
    },
    "BiLSTM": {
        "bilstm",
        "bi-lstm",
        "bidirectional lstm",
    },
    "Transformers": {
        "transformer models",
        "transformer architecture",
    },
    "Vector Databases": {
        "vector database",
        "vector databases",
        "vector db",
    },
    "Embeddings": {
        "embeddings",
        "semantic embeddings",
        "vector embeddings",
    },
    "Data Structures": {
        "data structures",
        "dsa",
    },
    "Algorithms": {
        "algorithms",
        "algorithm design",
    },
    "Object-Oriented Programming": {
        "object-oriented programming",
        "object oriented programming",
        "oop",
    },
    "Operating Systems": {
        "operating systems",
        "operating system",
        "os concepts",
    },
    "DBMS": {
        "dbms",
        "database management systems",
    },
    "Computer Networks": {
        "computer networks",
        "computer networking",
    },
    "System Design": {
        "system design",
        "software architecture",
    },
    "Multithreading": {
        "multithreading",
        "multi-threading",
        "multi threading",
    },
    "Concurrency": {
        "concurrency",
        "concurrent programming",
    },
    "Linux": {
        "linux",
        "unix",
    },
    "Git": {
        "git",
    },
    "GitHub": {
        "github",
        "git hub",
    },
    "Docker": {
        "docker",
        "containerization",
    },
    "Kubernetes": {
        "kubernetes",
        "k8s",
    },
    "AWS": {
        "aws",
        "amazon web services",
    },
    "Microsoft Azure": {
        "azure",
        "microsoft azure",
    },
    "Google Cloud": {
        "google cloud",
        "gcp",
        "google cloud platform",
    },
    "CI/CD": {
        "ci/cd",
        "continuous integration",
        "continuous deployment",
    },
    "Jenkins": {
        "jenkins",
    },
    "GitHub Actions": {
        "github actions",
    },
    "Testing": {
        "software testing",
        "unit testing",
        "integration testing",
    },
    "Pytest": {
        "pytest",
        "py test",
    },
    "Agile": {
        "agile",
        "scrum",
    },
}


def normalize_skill_text(value: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        value.strip().lower(),
    )


def canonicalize_skill_name(
    skill_name: str,
) -> str:
    normalized_name = normalize_skill_text(
        skill_name
    )

    for canonical_name, aliases in (
        SKILL_ALIASES.items()
    ):
        normalized_aliases = {
            normalize_skill_text(alias)
            for alias in aliases
        }

        normalized_aliases.add(
            normalize_skill_text(canonical_name)
        )

        if normalized_name in normalized_aliases:
            return canonical_name

    return skill_name.strip()


def alias_exists_in_text(
    original_text: str,
    normalized_text: str,
    alias: str,
) -> int | None:
    normalized_alias = normalize_skill_text(
        alias
    )

    if len(normalized_alias) == 1:
        uppercase_alias = normalized_alias.upper()

        match = re.search(
            rf"(?<![A-Za-z0-9])"
            rf"{re.escape(uppercase_alias)}"
            rf"(?![A-Za-z0-9])",
            original_text,
        )

        return (
            match.start()
            if match is not None
            else None
        )

    match = re.search(
        rf"(?<![a-z0-9])"
        rf"{re.escape(normalized_alias)}"
        rf"(?![a-z0-9])",
        normalized_text,
    )

    return (
        match.start()
        if match is not None
        else None
    )


def extract_skills(
    text: str,
    additional_skills: Iterable[str] | None = None,
) -> list[str]:
    original_text = text
    normalized_text = normalize_skill_text(text)

    searchable_skills: dict[str, set[str]] = {
        canonical_name: set(aliases)
        for canonical_name, aliases
        in SKILL_ALIASES.items()
    }

    if additional_skills is not None:
        for skill_name in additional_skills:
            cleaned_name = skill_name.strip()

            if not cleaned_name:
                continue

            canonical_name = canonicalize_skill_name(
                cleaned_name
            )

            searchable_skills.setdefault(
                canonical_name,
                set(),
            ).add(cleaned_name)

    detected_skills: list[
        tuple[int, str]
    ] = []

    for canonical_name, aliases in (
        searchable_skills.items()
    ):
        aliases_to_check = set(aliases)
        aliases_to_check.add(canonical_name)

        positions = [
            position
            for alias in aliases_to_check
            if (
                position := alias_exists_in_text(
                    original_text,
                    normalized_text,
                    alias,
                )
            )
            is not None
        ]

        if positions:
            detected_skills.append(
                (
                    min(positions),
                    canonical_name,
                )
            )

    detected_skills.sort(
        key=lambda item: (
            item[0],
            item[1].lower(),
        )
    )

    return [
        skill_name
        for _, skill_name in detected_skills
    ]