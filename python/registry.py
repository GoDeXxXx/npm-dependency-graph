import json
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

TIMEOUT = 15


# ошибка при обращении к репозиторию пакетов
class RegistryError(Exception):
    pass


# адрес описания последней версии пакета, "/" в имени с областью кодируется
def latest_url(base_url, name):
    return base_url.rstrip("/") + "/" + quote(name, safe="@") + "/latest"


# прямые зависимости пакета: поле dependencies его последней версии
def get_dependencies(base_url, name):
    url = latest_url(base_url, name)
    try:
        with urlopen(url, timeout=TIMEOUT) as response:
            data = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise RegistryError(f"пакет {name} не найден в репозитории "
                                f"{base_url}") from error
        raise RegistryError(f"репозиторий вернул ошибку {error.code} "
                            f"для пакета {name}") from error
    except URLError as error:
        raise RegistryError(f"не удалось подключиться к репозиторию "
                            f"{base_url}: {error.reason}") from error
    except (OSError, HTTPException) as error:
        raise RegistryError(f"ошибка при чтении ответа репозитория "
                            f"для пакета {name}: {error}") from error
    except ValueError as error:
        raise RegistryError(f"репозиторий вернул не JSON "
                            f"для пакета {name}") from error
    if not isinstance(data, dict):
        raise RegistryError(f"неверный формат описания пакета {name}")
    dependencies = data.get("dependencies") or {}
    if not isinstance(dependencies, dict):
        raise RegistryError(f"неверный формат зависимостей пакета {name}")
    return dependencies
