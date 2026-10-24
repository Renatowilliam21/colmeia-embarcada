/* PT-15.3.4: executor SIMULADO das ferramentas de apicultura.
 * Nenhuma operacao acessa sensores, rede ou atuadores.
 */
#include "colmeia_tools.h"

#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Le um inteiro estrito de um objeto JSON simples, sem aceitar valores
 * decimais, strings ou identificadores fora dos limites especificados.
 * Os argumentos sao produzidos pelo decodificador com gramatica restrita.
 */
static int ler_inteiro(const char *json, const char *chave,
                       int minimo, int maximo, int *saida)
{
    char campo[64];
    const char *p;
    char *fim;
    long valor;

    if (!json || !chave || !saida)
        return 0;
    if (snprintf(campo, sizeof(campo), "\"%s\"", chave) >= (int)sizeof(campo))
        return 0;

    p = strstr(json, campo);
    if (!p)
        return 0;
    p += strlen(campo);
    while (isspace((unsigned char)*p)) p++;
    if (*p++ != ':')
        return 0;
    while (isspace((unsigned char)*p)) p++;
    if (!isdigit((unsigned char)*p))
        return 0;

    errno = 0;
    valor = strtol(p, &fim, 10);
    if (errno == ERANGE || fim == p || valor < minimo || valor > maximo)
        return 0;
    while (isspace((unsigned char)*fim)) fim++;
    if (*fim != ',' && *fim != '}')
        return 0;

    *saida = (int)valor;
    return 1;
}

void colmeia_consultar_status(const char *args)
{
    int id;
    if (!ler_inteiro(args, "colmeia_id", 1, 50, &id)) {
        puts("ERR invalid_colmeia_id");
        fflush(stdout);
        return;
    }
    printf("ACT consultar_status_colmeia colmeia_id=%d simulated=1\n", id);
    printf("RESULT status colmeia_id=%d peso_kg=25.4 temperatura_c=34.2 umidade_pct=65.0 simulated=1\n", id);
    fflush(stdout);
}

void colmeia_listar_alertas(const char *args)
{
    (void)args;
    puts("ACT listar_colmeias_alerta simulated=1");
    puts("RESULT alertas colmeias=[3,7,12] simulated=1");
    fflush(stdout);
}

void colmeia_ativar_inspecao(const char *args)
{
    int id, duracao;
    if (!ler_inteiro(args, "colmeia_id", 1, 50, &id)) {
        puts("ERR invalid_colmeia_id");
        fflush(stdout);
        return;
    }
    if (!ler_inteiro(args, "duracao_min", 5, 60, &duracao)) {
        puts("ERR invalid_duracao_min");
        fflush(stdout);
        return;
    }
    printf("ACT ativar_modo_inspecao colmeia_id=%d duracao_min=%d simulated=1\n", id, duracao);
    printf("RESULT inspecao colmeia_id=%d duracao_min=%d status=simulated simulated=1\n", id, duracao);
    fflush(stdout);
}
