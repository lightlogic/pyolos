import click
from click.testing import CliRunner
from pyolosCLI import cli
from benedict import benedict


class TestCommandsHelps:

    def test_cli_help(self):

        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert 'Command line interface' in result.output

    def test_deposit_meta_help(self):

        runner = CliRunner()
        result = runner.invoke(cli, 'deposit-meta --help')
        assert result.exit_code == 0
        assert 'deposit-meta' in result.output

    def test_deposit_create_help(self):

        runner = CliRunner()
        result = runner.invoke(cli, 'deposit-create --help')
        assert result.exit_code == 0
        assert 'deposit-create' in result.output

    def test_deposit_delete_help(self):

        runner = CliRunner()
        result = runner.invoke(cli, 'deposit-delete --help')
        assert result.exit_code == 0
        assert 'deposit-delete' in result.output


class TestDeposit:

    def test_deposit_CreateMetaDelete(self):

        runner = CliRunner()
        result_create = runner.invoke(
            cli, "deposit-create --description 'If everything goes well, it should be killed soon.' --title 'pytest deposit'")
        created_deposit = benedict(result_create.output)
        assert result_create.exit_code == 0
        assert 'pytest deposit' in result_create.output

        result_meta = runner.invoke(cli, 'deposit-meta --resid ' + created_deposit['resId'])
        assert result_meta.exit_code == 0
        assert 'pytest deposit' in result_meta.output

        result_delete = runner.invoke(cli, 'deposit-delete --resid ' + created_deposit['resId'])
        assert result_delete.exit_code == 0
        assert created_deposit['resId'] in result_delete.output

class TestUpload:

    def test_dataset_Upload(self):

        runner = CliRunner()
        result_create = runner.invoke(
            cli, "deposit-create --description 'If everything goes well, it should be killed soon.' --title 'pytest deposit'")
        created_deposit = benedict(result_create.output)
        assert result_create.exit_code == 0
        assert 'pytest deposit' in result_create.output
        result_upload_primary = runner.invoke(cli, 'deposit-upload --file-category Primary --file-type Digitalized ' + created_deposit['resId'] + ' pyolos/test_data/ISS_March_2009_NASA_CC0.jpg')
        assert result_upload_primary.exit_code == 0
        assert 'ISS_March_2009_NASA_CC0.jpg' in result_upload_primary.output

        result_upload_meta = runner.invoke(cli, 'deposit-upload --file-category Package --file-type Metadata ' + created_deposit['resId'] + ' pyolos/test_data/dlcm.xml')
        assert result_upload_meta.exit_code == 0
        assert 'dlcm.xml' in result_upload_meta.output

        result_delete = runner.invoke(cli, 'deposit-delete --resid ' + created_deposit['resId'])
        assert result_delete.exit_code == 0
        assert created_deposit['resId'] in result_delete.output
