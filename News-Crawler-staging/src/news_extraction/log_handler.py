from utilities.common import get_logger

class LogHandler():
    def __init__(self) -> None:
        self.logger = get_logger("logs/crawler_v2.log")
        self.log_validated_article = get_logger("logs/validated_article.log")
        self.log_failed_article = get_logger("logs/failed_article.log")
        self.logger.info("_________Logging is started_________")
        self.log_validated_article.info("_________Logging is started_________")
        self.log_failed_article.info("_________Logging is started_________")
    
    def info(self, msg, log_in="crawler_v2"):
        """_summary_

        Args:
            msg (str): logging message
            log_in (str, optional): Possible values : 'crawler_v2' | 'validated_article' | 'failed_article'. Defaults to "crawler_v2".
        """
        if log_in == "crawler_v2":
            self.logger.info(msg)
        elif log_in == "validated_article":
            self.log_validated_article.info(msg)
        elif log_in == "failed_article":
            self.log_failed_article.info(msg)
    
    def error(self, msg, log_in="crawler_v2"):
        """_summary_

        Args:
            msg (str): logging message
            log_in (str, optional): Possible values : 'crawler_v2' | 'validated_article' | 'failed_article'. Defaults to "crawler_v2".
        """
        if log_in == "crawler_v2":
            self.logger.error(msg)
        elif log_in == "validated_article":
            self.log_validated_article.error(msg)
        elif log_in == "failed_article":
            self.log_failed_article.error(msg)

    def exception(self, msg, log_in="crawler_v2"):
        """_summary_

        Args:
            msg (str): logging message
            log_in (str, optional): Possible values : 'crawler_v2' | 'validated_article' | 'failed_article'. Defaults to "crawler_v2".
        """
        if log_in == "crawler_v2":
            self.logger.exception(msg)
        elif log_in == "validated_article":
            self.log_validated_article.exception(msg)
        elif log_in == "failed_article":
            self.log_failed_article.exception(msg)