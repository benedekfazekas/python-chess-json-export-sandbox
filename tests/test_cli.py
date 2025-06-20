from your_cli_tool.main import main_function

def test_main_function(capsys):
    main_function("test")
    captured = capsys.readouterr()
    assert "Processing input: test" in captured.out