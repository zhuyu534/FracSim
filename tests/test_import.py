"""测试模块导入是否正常"""
def test_import():
    from fracsim import main
    assert main.__name__ == "fracsim.main"