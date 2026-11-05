from 练习及收集.w3.log_manager.logger import Logger
from 练习及收集.w3.log_manager.config_tools import get_config
if __name__ == '__main__':
    cfg = get_config("config.json", default={"log_level": "INFO"})

    logger = Logger(
        name=cfg.get("app_name", "app"),
        log_file=cfg.get("log_file"),
        level=cfg.get("log_level", "INFO"),
    )
#指定内容演示，需要配合try使用
    logger.debug("细节信息，只在 DEBUG 级别显示")
    logger.info("程序启动完成")
    logger.warn("磁盘快满了")
    logger.error("连接超时")
#这个程序是当try抛出异常时，接住异常并写入指定内容
    try:
        raise ValueError("演示一个异常")
    except ValueError as e:
        logger.error(f"发生异常：{e}")